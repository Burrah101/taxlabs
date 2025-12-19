from flask import Flask, request, send_file, jsonify, redirect, url_for
from io import BytesIO
import pandas as pd
import traceback
import stripe

app = Flask(__name__)

# ✅ Stripe secret key (confirmed working from your terminal test)
stripe.api_key = "sk_test_51SfuJ1GXW2HJur5PrLI492yZpSN5OVbmcJPF4HARJVLCuIcuAFBnDJzWx4ka5UVGzCIJDkElv0vI9XDa2efEpSuN00ECDBsziU"
print(f"🔐 Stripe key in use: {stripe.api_key}")

# ✅ Stripe product price (in cents)
YOUR_PRICE = 300  # $3.00

@app.route("/checkout")
def checkout():
    try:
        print("⚙️  Creating Stripe Checkout session...")
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

@app.route("/upload", methods=["POST"])
def upload():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        df = pd.read_csv(file)

        from report_pdf import generate_pdf
        pdf_buffer = BytesIO()
        generate_pdf(df, pdf_buffer)
        pdf_buffer.seek(0)

        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='TaxLabs_Report.pdf'
        )

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": "Processing failed", "details": str(e)}), 500

if __name__ == "__main__":
    print("✅ This is the correct app.py")
    app.run(debug=True)
