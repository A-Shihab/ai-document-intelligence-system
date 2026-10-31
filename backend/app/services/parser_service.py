import os
import pandas as pd
from pypdf import PdfReader
from PIL import Image
import docx
from pptx import Presentation

class ParserService:
    @staticmethod
    def parse_file(file_path: str, file_extension: str) -> str:
        ext = file_extension.lower()
        text_content = ""

        try:
            # 1. PDF Files
            if ext == ".pdf":
                reader = PdfReader(file_path)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text_content += extracted + "\n"

            # 2. Excel Files (.xlsx, .xls)
            elif ext in [".xlsx", ".xls"]:
                df = pd.read_excel(file_path, sheet_name=None)
                for sheet_name, sheet_df in df.items():
                    text_content += f"\n--- Sheet: {sheet_name} ---\n"
                    text_content += sheet_df.to_string(index=False) + "\n"

            # 3. CSV Files
            elif ext == ".csv":
                df = pd.read_csv(file_path)
                text_content = df.to_string(index=False)

            # 4. Word Documents (.docx, .doc)
            elif ext in [".docx", ".doc"]:
                try:
                    doc = docx.Document(file_path)
                    lines = []
                    # Extract paragraph text
                    for para in doc.paragraphs:
                        if para.text.strip():
                            lines.append(para.text)
                    # Extract text inside table cells (crucial for Word invoice templates)
                    for table in doc.tables:
                        for row in table.rows:
                            row_cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                            if row_cells:
                                lines.append(" | ".join(row_cells))
                    text_content = "\n".join(lines)
                except Exception:
                    # Fallback plain text reading for legacy .doc files
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        text_content = f.read()

            # 5. PowerPoint Presentations (.pptx, .ppt)
            elif ext in [".pptx", ".ppt"]:
                prs = Presentation(file_path)
                slides_text = []
                for i, slide in enumerate(prs.slides):
                    slide_lines = [f"--- Slide {i+1} ---"]
                    for shape in slide.shapes:
                        if hasattr(shape, "text") and shape.text.strip():
                            slide_lines.append(shape.text.strip())
                    slides_text.append("\n".join(slide_lines))
                text_content = "\n\n".join(slides_text)

            # 6. Plain Text Files
            elif ext in [".txt", ".md"]:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    text_content = f.read()

            # 7. Images (.png, .jpg, .jpeg, .webp, .tiff, .bmp, etc.)
            elif ext in [".png", ".jpg", ".jpeg", ".webp", ".tiff", ".bmp"]:
                with Image.open(file_path) as img:
                    img.verify()
                text_content = f"[Multimodal Visual Document: {os.path.basename(file_path)}]"

            else:
                # General fallback attempt as plain text
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        text_content = f.read()
                except Exception:
                    text_content = f"Unsupported file format for direct parsing: {ext}"

        except Exception as e:
            text_content = f"Error parsing file: {str(e)}"

        return text_content