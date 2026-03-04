import pytest
from src.utils.pii_masker import mask_pii

def test_mask_pii_emails():
    text = "Contact me at test@example.com or user.name+tag@domain.co.uk"
    sanitized = mask_pii(text)
    assert "[EMAIL_MASKED]" in sanitized
    assert "test@example.com" not in sanitized
    assert "user.name+tag@domain.co.uk" not in sanitized

def test_mask_pii_phones():
    text = "Call +1-555-0199 or 07700 900123"
    sanitized = mask_pii(text)
    assert "[PHONE_MASKED]" in sanitized
    assert "+1-555-0199" not in sanitized
    assert "07700 900123" not in sanitized

def test_mask_pii_no_pii():
    text = "This is a clean string with no sensitive data."
    assert mask_pii(text) == text
