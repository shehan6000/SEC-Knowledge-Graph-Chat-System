import logging
import sys
from typing import Optional


def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """Setup logging configuration."""
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )
    
    return logging.getLogger(__name__)


def validate_question(question: str) -> tuple[bool, Optional[str]]:
    """Validate if a question is appropriate for the system."""
    if not question or not question.strip():
        return False, "Question cannot be empty"
    
    if len(question.strip()) < 3:
        return False, "Question is too short"
    
    if len(question) > 1000:
        return False, "Question is too long"
    
    # Add any additional validation rules here
    inappropriate_terms = ["password", "secret", "confidential"]
    if any(term in question.lower() for term in inappropriate_terms):
        return False, "Question contains inappropriate terms"
    
    return True, None