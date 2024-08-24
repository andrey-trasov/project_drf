import stripe

from myproject.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_prise(amount):
    """
    Создаем цену в страйпе
    """

    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": "Course Purchase"},
    )

def  create_stripe_session(price_id):
    """
    Создаем сессию для оплаты
    """
    session = stripe.checkout.Session.create(
        # payment_method_types=["card"],
        line_items=[ {"price": price_id,"quantity": 1,} ],
        mode="payment",
        success_url="http://127.0.0.1:8000/",
    )
    return session.id, session.url
