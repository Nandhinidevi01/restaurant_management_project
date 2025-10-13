import string
import secrets
from orders.models import Coupon  #Assuming you have a Coupon model
from .models import Order
from django.core.exceptions import ObjectDoesNotExist

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

def generate_unique_order_id(length=8):
    """
    Generate a unique, short alphanumeric ID for orders.

    Args:
        length (int): Length of the generated ID, Default is 8.

    Returns:
        str: A unique order ID.
    """
    characters = string.ascii_upperCase + string.digits
    while True:
        #generate a random string
        new_id = ''.join(secrets.choice(characters) for _ in range(length))

        #check if the ID already exixts in the database
        if not Order.objects.filter(order_id=new_id).exists():
            return new_id

logger = logging.getLogger(__name__)

def update_order_status(order_id, new_status):
    """
    Update the status of an order given its ID and a new status value.

    Args:
        order_id (int): The ID of the order to update.
        new_status (str): The new status to assign to the order.

    Returns:
        dict: A dictionary containing the result or error message.
    """
    try:
        #Retrieve the order from the database
        order = Order.objects.get(id=order_id)

        #store old status for logging
        old_status = order.status

        #update status
        order.status = new_status
        order.save()

        #Log the change
        logger.info(f"Order ID {order_id} status changed from '{old_status}' to '{new_status}'")

        return {
            "success": True,
            "message": f"Order {order_id} status updated successfully",
            "old_status": old_status,
            "new_status": new_status
        }
    except ObjectDoesNotExist:
        logger.error(f"order ID {order_id} not found.")
        return {
            "success": False,
            "error": "Order not found"
        }

    except Exception as e:
        logger.exception(f"Error updating order {order_id}: {e}")
        return {
            "success": False,
            "error": str(e)
        }