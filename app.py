from flask import Flask, request, send_file, jsonify, redirect, url_for
import pandas as pd
from io import BytesIO
from report_pdf import generate_pdf
import traceback
import stripe

print("✅ This is the correct app.py")

app = Flask(__name__)

# ✅ Stripe Secret Key — Sandbox
stripe.api_key = "sk_test_51sfuJ1GXW2HJur5PnDM1nTbr5P96PAUKWdpCe7gjiNzf9Mj3XE6xrWJ91cQpH8oy63y9j7A0yJ1koMSCQyTnCCTbo1h3t4XARLg100kUAsqDKPr"
YOUR_PRICE = 300  # $3.00 in cents

# ✅ Stripe Checkout Route
@app.route("/checkout")
def checkout():
    try:
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
            success_url=url_for('success', _external=True),
            cancel_url=url_for('cancel', _external=True),
        )
        return redirect(session.url, code=303)
    except Exception as e:
        print(f"Stripe Error: {e}")
        return "Something went wrong during checkout.", 500

# ✅ Payment Success Route
@app.route("/success")
def success():
    return "✅ Payment successful! You can now download your PDF."

# ✅ Payment Cancel Route
@app.route("/cancel")
def cancel():
    return "❌ Payment was cancelled. No charge was made."

# ✅ CSV Upload + PDF Generator
@app.route("/", methods=["GET"])
def index():
    return '''
    <html>
    <head><title>TaxLabs</title></head>
    <body style="background-color:#0e0e1d; color:white; font-family:sans-serif;">
    <center>
        <h1>TaxLabs</h1>
        <p>Upload your wallet CSV.<br>Get clarity in seconds.</p>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <br><br>
            <button type="submit" style="padding:10px 20px; background-color:#09f; color:white;">Generate Report</button>
        </form>
    </center>
    </body>
    </html>
    '''

@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files['file']
        if not file:
            return jsonify({"error": "No file uploaded"}), 400
        df = pd.read_csv(file)

        # ✅ In-memory PDF
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

# ✅ Test Route
@app.route("/test")
def test():
    return "✅ You are running the correct app.py"

# ✅ Run Server
if __name__ == "__main__":
    app.run(debug=True)
