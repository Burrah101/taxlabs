# app.py

from flask import Flask, redirect, url_for, send_file
import os
import stripe
from dotenv import load_dotenv
from report_pdf import generate_pdf

print("✅ app.py loaded")

# Load .env if present (for local development)
load_dotenv()

app = Flask(__name__)

# Stripe key from env
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
print("🔐 Stripe key loaded:", bool(stripe.api_key))

YOUR_PRICE = 300  # $3.00 in cents

@app.route("/")
def index():
    return "TaxLabs Home"

@app.route("/test")
def test():
    return "✅ You are running the correct app.py"

@app.route("/checkout")
def checkout():
    try:
        print("⚙️ Creating Stripe Checkout session...")
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "unit_amount": YOUR_PRICE,
                    "product_data": {"name": "Tax Report PDF"},
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=url_for("success", _external=True),
            cancel_url=url_for("cancel", _external=True),
        )
        print("✅ Stripe session created:", session.id)
        return redirect(session.url, code=303)
    except Exception as e:
        print("🔥 STRIPE ERROR:", repr(e))
        return "Something went wrong during checkout.", 500

@app.route("/success")
def success():
    print("💰 Payment succeeded. Generating PDF...")
    generate_pdf("static/report.pdf")
    return redirect(url_for("download_pdf"))

@app.route("/download")
def download_pdf():
    try:
        return send_file("static/report.pdf", as_attachment=True)
    except Exception as e:
        print("⚠️ PDF Download error:", repr(e))
        return "File not found.", 404

@app.route("/cancel")
def cancel():
    return "❌ Payment cancelled."

if __name__ == "__main__":
    app.run(debug=True)
