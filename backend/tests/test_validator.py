import pytest
from app.services.validator_service import ValidatorService

def test_validator_valid_invoice():
    valid_data = {
        "invoice_number": "INV-001",
        "invoice_date": "2026-10-30",
        "supplier_name": "Delta Office Supplies Ltd.",
        "subtotal": 1000.0,
        "discount": 100.0,
        "tax": 90.0,
        "shipping": 0.0,
        "total": 990.0
    }
    errors = ValidatorService.validate_extracted_data(valid_data)
    assert len(errors) == 0

def test_validator_missing_mandatory_fields():
    incomplete_data = {
        "invoice_number": "",
        "invoice_date": "2026-10-30",
        "supplier_name": None,
        "total": 500.0
    }
    errors = ValidatorService.validate_extracted_data(incomplete_data)
    error_fields = [e["field"] for e in errors]
    assert "invoice_number" in error_fields
    assert "supplier_name" in error_fields

def test_validator_mathematical_mismatch():
    mismatched_data = {
        "invoice_number": "INV-ERR-001",
        "invoice_date": "2026-10-30",
        "supplier_name": "Test Supplier",
        "subtotal": 1000.0,
        "discount": 0.0,
        "tax": 100.0,
        "shipping": 0.0,
        "total": 2000.0
    }
    errors = ValidatorService.validate_extracted_data(mismatched_data)
    assert any(e["field"] == "total" for e in errors)