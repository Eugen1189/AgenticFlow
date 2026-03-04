import re
import structlog

logger = structlog.get_logger()

def mask_pii(text: str) -> str:
    """
    Mask Personal Identifiable Information (PII) for GDPR compliance.
    
    Currently handles:
    - Emails
    - Phone numbers (basic international format)
    
    Args:
        text: The input text to be sanitized.
        
    Returns:
        The sanitized text with PII masked by [MASKED].
    """
    log = logger.bind(utility="pii_masker")
    
    # Regex for email
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    # Regex for phone (simple version)
    phone_pattern = r'\+?\d[\d -]{7,}\d'
    
    sanitized = re.sub(email_pattern, "[EMAIL_MASKED]", text)
    sanitized = re.sub(phone_pattern, "[PHONE_MASKED]", sanitized)
    
    if sanitized != text:
        log.info("pii_masked", original_length=len(text), result_length=len(sanitized))
    
    return sanitized
