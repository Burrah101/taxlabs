import stripe
from flask import redirect, url_for

stripe.api_key = "PASTE_REAL_sk_test_KEY_HERE"
YOUR_PRICE = 300  # $3.00

@app.route("/checkout")
def checkout():
    try:
        print("Using Stripe key:", stripe.api_key[:12], "...")

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "unit_amount": YOUR_PRICE,
                    "product_data": {
                        "name": "Tax Report PDF"
                    },
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=url_for("success", _external=True),
            cancel_url=url_for("cancel", _external=True),
        )

        return redirect(session.url, code=303)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return "Something went wrong during checkout.", 500


@app.route("/success")
def success():
    return "✅ Payment successful!"


@app.route("/cancel")
def cancel():
    return "❌ Payment cancelled."
