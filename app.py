from flask import Flask, redirect, url_for, send_from_directory
import os
import stripe
from report_pdf import generate_pdf

print("✅ app.py loaded")

app = Flask(__name__)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
print("🔐 Stripe key loaded:", bool(stripe.api_key))

YOUR_PRICE = 300

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
    # This creates the PDF after payment
    generate_pdf()
    return redirect("/download")

@app.route("/download")
def download():
    return send_from_directory("static", "report.pdf", as_attachment=True)

@app.route("/cancel")
def cancel():
    return "❌ Payment cancelled."

if __name__ == "__main__":
    app.run(debug=True)
