from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
import logging
from datetime import datetime, time
from home.utils import is_restaurant_open

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

def is_restaurant_open():
    """
    Check if the restaurant is currently open based on operating hours.

    Returns:
        bool: True if open, False if closed.
    """

    #get current day and time
    now = datetime.now()
    current_time = now.time()
    current_day = now.strftime("%A")

    opening_hours = {
        "Monday":    (time(9,0), time(22,0)),
        "Tuesday":   (time(9,0), time(22,0)),
        "Wednesday": (time(9,0), time(22,0)),
        "Thursday":  (time(9,0), time(22,0)),
        "Friday":    (time(9,0), time(23,0)),
        "Saturday":  (time(9,0), time(23,0)),
        "Sunday":    (time(10,0), time(21,0)),
    }

    #Get today's hours
    if current_day not in opening_hours:
        return False

    open_time, close_time = opening_hours[current_day]

    return open_time <= current_time <= close_time

print(is_restaurant_open())