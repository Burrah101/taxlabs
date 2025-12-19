from flask import Flask, request, send_file, jsonify, redirect, url_for
import pandas as pd
import traceback
from io import BytesIO
import stripe

app = Flask(__name__)

# ✅ Stripe Config
stripe.api_key = "sk_test_51sfuJ1GXW2HJur5PnDM1nTbr5P96PAUKWdpCe7gjiNzf9Mj3XE6xrWJ91cQpH8oy63y9j7A0yJ1koMSCQyTnCCTbo1h3t4XARLg100kUAsqDKPr"
YOUR_PRICE = 300  # $3.00 in cents

@app.route("/")
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>TaxLabs</title>
        <style>
            body { background-color: #0e0e1d; color: white; font-family: Arial; text-align: center; padding-top: 50px; }
            input[type="file"] { margin: 20px auto; display: block; }
            button { background-color: #09f; color: white; padding: 10px 20px; border: none; cursor: pointer; font-size: 16px; }
        </style>
    </head>
    <body>
        <h1>TaxLabs</h1>
        <p>Upload your wallet CSV.<br>Get clarity in seconds.</p>
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <button type="submit">Generate Report</button>
        </form>
    </body>
    </html>
    '''

@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files['file']
        df = pd.read_csv(file)

        # Create in-memory buffer
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
                    "product_data": {"name": "Tax Report PDF"},
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

@app.route("/success")
def success():
    return "✅ Payment successful! You can now download your PDF."

@app.route("/cancel")
def cancel():
    return "❌ Payment was cancelled. No charge was made."

# ✅ PDF Generator using reportlab
from reportlab.pdfgen import canvas
def generate_pdf(df, buffer):
    c = canvas.Canvas(buffer)
    c.drawString(100, 800, "Tax Report Summary")

    y = 750
    for index, row in df.iterrows():
        line = f"{row['date']} | {row['type']} | {row['asset']} | ${row['usd_value']}"
        c.drawString(100, y, line)
        y -= 20

    c.save()

# ✅ Debug route to confirm right file
@app.route("/test")
def test():
    return "✅ You are running the correct app.py"

# ✅ Start the app
if __name__ == "__main__":
    app.run(debug=True)
