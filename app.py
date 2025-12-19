from flask import Flask, redirect, url_for
import stripe

print("✅ app.py loaded")

app = Flask(__name__)

# 🔐 STRIPE KEY - Store as single string
STRIPE_SECRET_KEY = "sk_test_51SfuJ1GXW2HJur5PrLI492yZpSN5OVbmcJPF4HARJVLCuIcuAFBnDJzWx4ka5UVGzCIJDkElv0vI9XDa2efEpSuN00ECDBsziU"

stripe.api_key = STRIPE_SECRET_KEY

print("🔐 Stripe key length:", len(STRIPE_SECRET_KEY))
print("🔐 Stripe key starts with:", STRIPE_SECRET_KEY[:15])
print("🔐 Stripe key ends with:", STRIPE_SECRET_KEY[-10:])

YOUR_PRICE = 300  # $3.00

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
        print("✅ Stripe session created:", session.id)
        return redirect(session.url, code=303)
    except stripe.error.StripeError as e:
        print("🔥 STRIPE ERROR:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")
        return f"Stripe Error: {str(e)}", 500
    except Exception as e:
        print("🔥 UNEXPECTED ERROR:")
        print(repr(e))
        return "Something went wrong during checkout.", 500

@app.route("/success")
def success():
    return "✅ Payment successful!"

@app.route("/cancel")
def cancel():
    return "❌ Payment cancelled."

if __name__ == "__main__":
    app.run(debug=True)
