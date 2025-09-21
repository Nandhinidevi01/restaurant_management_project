import string
import secrets
from orders.models import Coupon  #Assuming you have a Coupon model

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