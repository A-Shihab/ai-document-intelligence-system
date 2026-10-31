import os
import shutil
import asyncio
import math
from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from google import genai
from google.genai import types
from app.database import get_db, AsyncSessionLocal
from app.config import settings
from app.models.document import DocumentModel
from app.services.parser_service import ParserService
from app.services.gemini_service import GeminiService
from app.services.validator_service import ValidatorService

router = APIRouter()
gemini_service = GeminiService()
genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)

EMBEDDING_MODEL = "gemini-embedding-2"
EMBEDDING_DIMENSIONS = 384

class SearchRequest(BaseModel):
    query: str

async def generate_embedding(text: str, is_query: bool = True) -> list[float]:
    if not text or not text.strip():
        raise ValueError("Cannot generate an embedding from empty text.")
    
    prefix = "task: search query | text: " if is_query else "task: document indexing | text: "
    prepared_text = prefix + text.strip()
    
    try:
        response = await asyncio.to_thread(
            genai_client.models.embed_content,
            model=EMBEDDING_MODEL,
            contents=prepared_text,
            config=types.EmbedContentConfig(
                output_dimensionality=EMBEDDING_DIMENSIONS
            ),
        )
    except Exception as exc:
        print(f"Embedding API failed: {type(exc).__name__}: {exc}")
        raise RuntimeError("Gemini embedding generation failed.") from exc

    embeddings = getattr(response, "embeddings", None)
    if not embeddings:
        raise RuntimeError("Gemini returned no embeddings.")
    
    values = getattr(embeddings[0], "values", None)
    if not values:
        raise RuntimeError("Gemini embedding values are empty.")

    return [float(v) for v in values]

async def run_pipeline(doc_id: int, file_path: str, file_ext: str):
    ext = file_ext.lower()
    print(f"--- STARTING PIPELINE FOR DOC {doc_id} ({file_path}) ---")
    
    try:
        text_content = ParserService.parse_file(file_path, file_ext)
        
        if ext in [".png", ".jpg", ".jpeg", ".webp", ".tiff", ".bmp"]:
            extracted_json = await gemini_service.extract_document_data(
                content_input=text_content, 
                file_path=file_path, 
                is_image=True
            )
            if "error" not in extracted_json:
                text_content = (
                    f"Invoice Number: {extracted_json.get('invoice_number')}\n"
                    f"Supplier: {extracted_json.get('supplier_name')}\n"
                    f"Customer: {extracted_json.get('customer_name')}\n"
                    f"Total: {extracted_json.get('currency', '')} {extracted_json.get('total')}\n"
                    f"Date: {extracted_json.get('invoice_date')}"
                )
        else:
            extracted_json = await gemini_service.extract_document_data(
                content_input=text_content, 
                is_image=False
            )
        
        validation_results = ValidatorService.validate_extracted_data(extracted_json)
        
        embedding_vector = None
        try:
            embedding_vector = await generate_embedding(text_content, is_query=False)
        except Exception as exc:
            print(f"Embedding failed for document {doc_id}: {type(exc).__name__}")
            validation_results.append({
                "field": "embedding",
                "error": "Embedding generation failed. Semantic search unavailable.",
            })

        async with AsyncSessionLocal() as session:
            result = await session.execute(select(DocumentModel).where(DocumentModel.id == doc_id))
            doc = result.scalars().first()
            if doc:
                doc.raw_text = text_content
                doc.extracted_data = extracted_json
                doc.validation_errors = validation_results
                doc.embedding = embedding_vector
                doc.status = "COMPLETED" if not validation_results else "FLAGGED"
                await session.commit()
                print(f"--- PIPELINE COMPLETED FOR DOC {doc_id} ---")
    except Exception as e:
        print(f"!!! PIPELINE CRASHED FOR DOC {doc_id}: {str(e)} !!!")
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(DocumentModel).where(DocumentModel.id == doc_id))
            doc = result.scalars().first()
            if doc:
                doc.validation_errors = [{"field": "general", "error": f"Pipeline crashed: {str(e)}"}]
                doc.status = "FLAGGED"
                await session.commit()

@router.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # Prevent duplicate filename uploads
    existing_result = await db.execute(
        select(DocumentModel).where(DocumentModel.filename == file.filename)
    )
    existing_doc = existing_result.scalars().first()
    if existing_doc:
        raise HTTPException(
            status_code=400,
            detail=f"A document with the filename '{file.filename}' has already been uploaded (Document ID #{existing_doc.id})."
        )

    file_ext = os.path.splitext(file.filename)[1].lower()
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_doc = DocumentModel(
        filename=file.filename,
        file_type=file_ext.replace(".", ""),
        file_path=file_path,
        status="PROCESSING"
    )
    db.add(new_doc)
    await db.commit()
    await db.refresh(new_doc)

    background_tasks.add_task(run_pipeline, new_doc.id, file_path, file_ext)

    return {"message": "Document uploaded and processing started successfully.", "document_id": new_doc.id}

@router.get("")
@router.get("/")
async def get_all_documents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DocumentModel))
    documents = result.scalars().all()
    return documents

@router.post("/search")
async def search_documents(
    search: SearchRequest,
    db: AsyncSession = Depends(get_db),
):
    query_text = search.query.strip()
    if not query_text:
        return []
    
    try:
        query_embedding = await generate_embedding(query_text, is_query=True)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Could not generate search embedding.") from exc

    distance = DocumentModel.embedding.cosine_distance(query_embedding)
    statement = (
        select(DocumentModel)
        .where(DocumentModel.embedding.is_not(None))
        .order_by(distance)
        .limit(3)
    )
    result = await db.execute(statement)
    documents = result.scalars().all()

    query_lower = query_text.lower()
    scored_docs = []
    for doc in documents:
        score = 0.0
        if doc.raw_text and any(word in doc.raw_text.lower() for word in query_lower.split() if len(word) > 3):
            score += 1.0
        if doc.extracted_data and isinstance(doc.extracted_data, dict):
            supplier = str(doc.extracted_data.get("supplier_name", "")).lower()
            if supplier and any(term in query_lower for term in supplier.split()):
                score += 3.0
        scored_docs.append((score, doc))

    scored_docs.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in scored_docs]

@router.delete("/{doc_id}")
async def delete_document(doc_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DocumentModel).where(DocumentModel.id == doc_id))
    doc = result.scalars().first()
    if not doc:
        return {"error": "Document not found"}
    
    if doc.file_path and os.path.exists(doc.file_path):
        try:
            os.remove(doc.file_path)
        except Exception:
            pass

    await db.delete(doc)
    await db.commit()
    return {"message": f"Document {doc_id} deleted successfully."}