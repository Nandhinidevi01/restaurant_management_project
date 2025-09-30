from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_email(recipient_email, subject, message_body, from_email=None):
    """
    Utility function to send an email,
    :param recipient email: str | list of emails
    :param subject: str - Subject of the email
    :param message_body: str - Email body content
    :param from_email: str (optional) - Defaults to settings.DEFAULT_FROM_EMAIL
    :return True if sent successfully, False otherwise
    """
    try:
        if not from_email:
            from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(
            subject,
            message_body,
            from_email,
            [recipient_email] if isinstance(recipient_email, str) else recipient_email,
            fail_silently=False,
        )
        return True
    except BadHeaderError:
        logger.error("Invalid header found while sending email.")
        return False
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False