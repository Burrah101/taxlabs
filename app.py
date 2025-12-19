import stripe
from flask import Flask, request, redirect, url_for

import requests
import ssl
from stripe.http_client import RequestsClient

# Flask app
app = Flask(__name__)

# Force Stripe to use clean HTTPS client
stripe.default_http_client = RequestsClient()
stripe.verify_ssl_certs = True

# ✅ Stripe API Key from your dashboard (confirmed working in Python shell)
stripe.api_key = "sk_test_51SfuJ1GXW2HJur5PrLI492yZpSN5OVbmcJPF4HARJVLCuIcuAFBnDJzWx4ka5UVGzCIJDkElv0vI9XDa2efEpSuN00ECDBsziU"
print(f"🔐 Stripe key in use: {stripe.api_key}")

@app.route("/checkout")
def checkout():
    try:
        print("⚙️  Creating Stripe Checkout session...")
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "unit_amount": 300,
                    "product_data": {"name": "Tax Report PDF"},
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=url_for("success", _external=True),
            cancel_url=url_for("cancel", _external=True),
        )
        print("✅ Stripe session created.")
        return redirect(session.url, code=303)
    except Exception as e:
        print("🔥 Stripe ERROR:")
        print(str(e))  # full error
        return "Something went wrong during checkout.", 500

@app.route("/success")
def success():
    return "✅ Payment was successful!"

@app.route("/cancel")
def cancel():
    return "❌ Payment was cancelled."
