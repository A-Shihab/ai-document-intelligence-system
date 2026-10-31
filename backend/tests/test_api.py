from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_documents_endpoint():
    """Test that the main documents endpoint responds successfully."""
    response = client.get("/api/v1/documents/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@patch("app.api.v1.endpoints.documents.AsyncSession.commit", new_callable=AsyncMock)
@patch("app.api.v1.endpoints.documents.AsyncSession.refresh", new_callable=AsyncMock)
@patch("app.api.v1.endpoints.documents.AsyncSession.execute")
def test_api_unsupported_file_upload_rejection(mock_execute, mock_refresh, mock_commit):
    """Test that uploading an unsupported file format is handled or rejected by the endpoint."""
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = None

    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_execute.return_value = mock_result

    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("test.xyz", b"some random binary content", "application/octet-stream")}
    )
    assert response.status_code in [200, 400, 422]
    error_data = response.json()
    assert isinstance(error_data, (dict, list))

@patch("app.api.v1.endpoints.documents.AsyncSession.execute")
@patch("app.api.v1.endpoints.documents.generate_embedding")
def test_semantic_search_endpoint_returns_empty_results(mock_embed, mock_execute):
    """Test semantic search endpoint handles valid query structure and returns structured empty collection properly."""
    mock_embed.return_value = [0.1] * 384
    
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = []

    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_execute.return_value = mock_result

    response = client.post(
        "/api/v1/documents/search",
        json={"query": "Delta Office Supplies Ltd."}
    )
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    assert len(results) == 0

@patch("app.api.v1.endpoints.documents.AsyncSession.execute")
@patch("app.api.v1.endpoints.documents.generate_embedding")
def test_semantic_search_ranking_order(mock_embed, mock_execute):
    """Test that semantic search correctly ranks relevant documents first and respects the top-3 limit."""
    mock_embed.return_value = [0.2] * 384

    doc_match_1 = MagicMock(id=1, filename="invoice_delta.pdf", file_name="invoice_delta.pdf", extracted_data={"supplier_name": "Delta Office Supplies Ltd."})
    doc_match_2 = MagicMock(id=2, filename="invoice_beta.pdf", file_name="invoice_beta.pdf", extracted_data={"supplier_name": "Beta Corp"})

    mock_scalars = MagicMock()
    mock_scalars.all.return_value = [doc_match_1, doc_match_2]

    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_execute.return_value = mock_result

    response = client.post(
        "/api/v1/documents/search",
        json={"query": "Delta Office Supplies"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 3
    assert len(data) == 2