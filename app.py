from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
import traceback
import pandas as pd
import stripe
from io import BytesIO
from report_pdf import generate_pdf

app = Flask(__name__)

# ✅ Stripe Test Secret Key (standard, working)
stripe.api_key = "sk_test_51SfuJ1GXW2HJur5PrLI492yZpSN5OVbmcJPF4HARJVLCuIcuAFBnDJzWx4ka5UVGzCIJDkElv0vI9XDa2efEpSuN00ECDBsziU"
YOUR_PRICE = 300

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files["file"]
        df = pd.read_csv(file)
        pdf_buffer = BytesIO()
        generate_pdf(df, pdf_buffer)
        pdf_buffer.seek(0)
        return send_file(pdf_buffer, mimetype="application/pdf", as_attachment=True, download_name="TaxLabs_Report.pdf")
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": "Processing failed", "details": str(e)}), 500

@app.route("/checkout")
def checkout():
    try:
        print("⚙️  Creating Stripe Checkout session...")  # ✅ DEBUG print
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
        print("✅ Stripe session created.")
        return redirect(session.url, code=303)
    except Exception as e:
        print(f"Stripe Error: {e}")
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
    print("✅ This is the correct app.py")
    app.run(debug=True)
