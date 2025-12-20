from flask import Flask, redirect, url_for
import stripe

app = Flask(__name__)

stripe.api_key = "sk_test_51SfuJ1GXW2HJur5PrLI492yZpSN5OVbmcJPF4HARJVLCuIcuAFBnDJzWx4ka5UVGzCIJDkElv0vI9XDa2efEpSuN00ECDBsziU"
print("🔐 LIVE STRIPE KEY:", stripe.api_key)

@app.route("/
test")
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
                    "unit_amount": 500,
                    "product_data": {"name": "PDF"},
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
    return "✅ Payment successful!"

@app.route("/cancel")
def cancel():
    return "❌ Payment canceled."

if __name__ == "__main__":
    app.run(debug=True)
