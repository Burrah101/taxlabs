import stripe
from flask import redirect, url_for

print("✅ Stripe block loaded")

# Your Flask app init (ensure this is already above)
# app = Flask(__name__)

# ✅ Real working secret key (test mode)
stripe.api_key = "sk_test_51SfuJ1GXW2HJur5PrLI492yZpSN5OVbmcJPF4HARJVLCuIcuAFBnDJzWx4ka5UVGzCIJDkElv0vI9XDa2efEpSuN00ECDBsziU"

# Confirm key is printing properly
print(f"🔐 Stripe key in use: {stripe.api_key}")

# Stripe checkout route
@app.route("/checkout")
def checkout():
    try:
        print("⚙️  Creating Stripe Checkout session...")
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "unit_amount": 300,  # $3.00
                    "product_data": {
                        "name": "Tax Report PDF"
                    },
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=url_for('success', _external=True),
            cancel_url=url_for('cancel', _external=True),
        )
        print("✅ Stripe session created.")
        return redirect(session.url, code=303)

    except Exception as e:
        print(f"❌ Stripe Error: {e}")  # Shows the real error in terminal
        return "Something went wrong during checkout.", 500

# Success + cancel pages
@app.route("/success")
def success():
    return "✅ Payment successful! You can now download your PDF."

@app.route("/cancel")
def cancel():
    return "❌ Payment was cancelled. No charge was made."
