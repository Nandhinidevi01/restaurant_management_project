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

def calculate_discount(original_price, discount_percentage):
    """
    Calculate the discounted price based on the original price and discount percentage.

    Args:
        original_price (float): The original price of the item.
        discount_percentage (float): The discount_percentage to apply (0-100).

    Returns:
        Float: The discounted price rounded to 2 decimal places.
        OR
        str: An error message if input is invalid.
    """

    try:
        # Validate input types
        if not isinstance(original_price, (int, float)) or not isinstance(discount_percentage, (int, float)):
            return "Error: Both inputs must be numbers."

        #Validate input ranges
        if original_price < 0:
            return "Error: Original price cannot be negative."
        if discount_percentage < 0 or discount_percentage > 100:
            return "Error: Discount percentage must be between 0 and 100."

        #Calculate discounted price
        discount_price = original_price - (original_price * (discount_percentage/100))
        return round(discount_price, 2)

    except Exception as e:
        #Catch unexpected errors
        return f"Error: {str(e)}"