import logging
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

#configure logger
logger = logging.getLogger(__name__)

def validate_email_address(email: str) -> bool:
    """
    Validates an email address using Django's built-in EmailValidator.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    validator = EmailValidator()
    try:
        validator(email)
        return True
    except ValidationError as e:
        logger.warning(f"Invalid email attempted: {email}. Error: {e}")
        return False