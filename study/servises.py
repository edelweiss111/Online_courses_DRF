import os

import stripe


def create_payment(obj, user):
    stripe.api_key = os.getenv('STRIPE_API_KEY')
    create_product = stripe.Product.create(
        name=obj.name,
    )

    price = stripe.Price.create(
        unit_amount=int(obj.amount)*100,
        currency='rub',
        product=create_product['id'],
    )

    session = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[
            {
                "price": price.id,
                "quantity": 1
            }
        ],
        mode="payment",
        client_reference_id=user.id
    )
    return session


def check_payment(session_id):
    stripe.api_key = os.getenv('STRIPE_API_KEY')

    session = stripe.checkout.Session.retrieve(session_id)

    return session
