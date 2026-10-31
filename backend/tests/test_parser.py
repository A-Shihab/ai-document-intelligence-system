import os
import pytest
from app.services.parser_service import ParserService

def test_parser_unsupported_format(tmp_path):
    """Test that unsupported file extensions return appropriate fallback or error behavior."""
    file_path = os.path.join(tmp_path, "test.xyz")
    with open(file_path, "w") as f:
        f.write("random content")
    
    content = ParserService.parse_file(file_path, ".xyz")
    assert content is not None