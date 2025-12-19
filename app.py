from flask import Flask, redirect, url_for
import stripe
import traceback

# -------------------------
# Flask App
# -------------------------
app = Flask(__name__)
print("APP STARTED - correct app.py loaded")

# -------------------------
# Stripe Configuration
# -------------------------
# IMPORTANT:
# Replace this with YOUR WORKING sk_test_ key
stripe.api_key = "PUT_YOUR_sk_test_KEY_HERE"

PRICE_CENTS = 300  # $3.00

print("Stripe key loaded:", stripe.api_key[:12], "...")

# -------------------------
# Routes
# -------------------------
@app.route("/")
def index():
    return """
    <h1>Stripe Test</h1>
    <a href="/checkout">Go to Checkout</a>
    """

@app.route("/test")
def test():
    return "TEST ROUTE OK"

@app.route("/checkout")
def checkout():
    try:
        print("Creating Stripe Checkout Session...")

        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "unit_amount": PRICE_CENTS,
                    "product_data": {
                        "name": "Tax Report PDF"
                    },
                },
                "quantity": 1,
            }],
            success_url=url_for("success", _external=True),
            cancel_url=url_for("cancel", _external=True),
        )

        print("Checkout session created:", session.id)
        print("Redirect URL:", session.url)

        return redirect(session.url, code=303)

    except Exception as e:
        print("STRIPE ERROR:")
        traceback.print_exc()
        return "Checkout failed. See server logs.", 500

@app.route("/success")
def success():
    return "PAYMENT SUCCESS"

@app.route("/cancel")
def cancel():
    return "PAYMENT CANCELLED"

# -------------------------
# Run Local Server
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
