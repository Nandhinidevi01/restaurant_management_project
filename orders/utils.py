import string
import secrets
from orders.models import Coupon  #Assuming you have a Coupon model
from django.db.models import Sum
from .models import Order
from datetime import date
from orders.utils import get_daily_sales_total

def generate_coupon_code(length=10):
    """
    Generate a unique alphanumeric coupon code.

    Args:
        lenght (int): The length of the coupon code (default = 10).

    Returns:
        str: A unique coupon code string.
    """
    characters = string.ascii_upperCase + string.digits #A-Z, 0-9

    while True:
        #Generate random coupon
        code = ''.join(secrets.choice(characters) for _ in range(lenght))

        #check uniqueness in DB (Coupon model must have a 'code' field)
        if not Coupon.objects.filter(code=code).exists():
            return code

from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_order_confirmation_email(order_id, customer_email, user_name, total_price):
    """
    Sends an order confirmation email to the customer.
    """
    subject = f"Order Confirmation - Order #{order_id}"
    message = (
        f"Hello {user_name},\n\n"
        f"Thank you for your order!\n"
        f"Your order ID is {order_id},\n"
        f"Total Price: ${total_price}\n\n"
        f"We will notify you once your order is processed.\n\n"
        f"Best regards,\n"
        f"The Restaurant Team"
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [customer_email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return {"success": True, "message": "Order confirmation email sent successfully."}
    except BadHeaderError:
        logger.error(f"Invalid header found when sending email to {customer_email}")
        return {"success": False, "message": "Invalid email header."}
    except Exception as e:
        logger.error(f"Error sending order confirmation email: {e}")
        return {"success": False, "message": f"Failed to send email: {e}"}

def get_daily_sales_total(date):
    """
    Calculate total sales for a given day.

    Args:
        date (datetime.date): The date for which sales should be calculated.

    Returns:
        Decimal: Total sales for the day. Returns 0 if no orders found.
    """
    total = (
        Order.objects.filter(created_at_date=date)
        .aggregate(total_sum=Sum('total_price'))
        .get('total_sum')
    )
    return total or 0

today = date.today()
print(get_daily_sales_total(today))