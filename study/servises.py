import os

import stripe


def create_payment(product, user):

    stripe.api_key = os.getenv('STRIPE_API_KEY')

    product = stripe.Product.create(
        name=product.name,
    )

    price = stripe.Price.create(
        unit_amount=product.amount,
        currency='rub',
        product=product['id'],
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
        client_reference_id=user
    )
