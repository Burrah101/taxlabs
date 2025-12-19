import stripe
from flask import Flask, request, redirect, url_for, jsonify

app = Flask(__name__)
print("✅ This is the correct app.py")

# ✅ Stripe Secret Key (paste the fresh sk_test key here)
stripe.api_key = "sk_test_51SfuJ1GXW2HJur5PrLI492yZpSN5OVbmcJPF4HARJVLCuIcuAFBnDJzWx4ka5UVGzCIJDkElv0vI9XDa2efEpSuN00ECDBsziU"

YOUR_PRICE = 300  # in cents ($3.00)

@app.route("/checkout")
def checkout():
    try:
        print("🚀 Creating Stripe Checkout session...")
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
            success_url=url_for('success', _external=True),
            cancel_url=url_for('cancel', _external=True),
        )
        print("✅ Stripe session created:", session.id)
        return redirect(session.url, code=303)
    except Exception as e:
        print("❌ Stripe Error:", e)
        return "Something went wrong during checkout.", 500

@app.route("/success")
def success():
    return "✅ Payment successful! You can now download your PDF."

@app.route("/cancel")
def cancel():
    return "❌ Payment was cancelled. No charge was made."

@app.route("/test")
def test():
    return "✅ You are running the correct app.py"

if __name__ == "__main__":
    app.run(debug=True)
