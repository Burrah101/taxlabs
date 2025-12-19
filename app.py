from flask import Flask, request, send_file, jsonify, redirect, url_for
import stripe

app = Flask(__name__)

# ✅ Real Stripe secret key (from your Stripe dashboard screenshot)
stripe.api_key = "sk_test_51SfuJ1GXW2HJur5PrLI492yZpSN5OVbmcJPF4HARJVLCuIcuAFBnDJzWx4ka5UVGzCIJDkElv0vI9XDa2efEpSuN00ECDBsziU"
print(f"🔐 Stripe key in use: {stripe.api_key}")

# ✅ Test route to confirm correct file
@app.route("/test")
def test():
    return "✅ You are running the correct app.py"

# ✅ Full Stripe Checkout Route with DEBUG
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
        print(f"❌ STRIPE ERROR: {e}")
        return "Something went wrong during checkout.", 500

# ✅ Success and Cancel routes
@app.route("/success")
def success():
    return "✅ Payment successful! You can now download your PDF."

@app.route("/cancel")
def cancel():
    return "❌ Payment was cancelled. No charge was made."

# ✅ App entry point
if __name__ == "__main__":
    print("✅ This is the correct app.py")
    app.run(debug=True)
