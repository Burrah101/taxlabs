from flask import Flask, redirect, url_for
import stripe

print("✅ app.py loaded")

app = Flask(__name__)

# ✅ Stripe Key — copy your full working key here
stripe.api_key = "sk_test_51SfuJ1GXW2HJur5Pq9oEqwDjv1abc123XYZabcDEFabc4567h0vI9XDa2efEpSuN00ECDBsziU"

# 💡 Debug to confirm runtime key
print("🔐 Stripe key preview:", stripe.api_key[:12])
print("🔐 Stripe key length:", len(stripe.api_key))

@app.route("/")
def home():
    return "✅ TaxLabs app is running"

@app.route("/checkout")
def checkout():
    try:
        print("⚙️ Creating Stripe session...")
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "unit_amount": 500,
                    "product_data": {
                        "name": "PDF Report"
                    },
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=url_for("success", _external=True),
            cancel_url=url_for("cancel", _external=True),
        )
        print("✅ Session created:", session.id)
        return redirect(session.url, code=303)
    except Exception as e:
        print("🔥 STRIPE ERROR:", repr(e))
        return "Something went wrong during checkout.", 500

@app.route("/success")
def success():
    return "✅ Payment was successful!"

@app.route("/cancel")
def cancel():
    return "❌ Payment was cancelled!"

if __name__ == "__main__":
    app.run(debug=True)
