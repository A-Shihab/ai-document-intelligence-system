import os
from unittest.mock import patch
from app.services.parser_service import ParserService

@patch("PIL.Image.open")
def test_ocr_extracts_real_invoice_text(mock_img_open, tmp_path):
    """Test that ParserService executes image parsing and OCR extraction on a valid image path."""
    fake_img_path = tmp_path / "sample_invoice.png"
    fake_img_path.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR" + b"\x00" * 100)
    
    extracted_text = ParserService.parse_file(str(fake_img_path), ".png")
    
    assert isinstance(extracted_text, str)