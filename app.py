from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
import pandas as pd
import traceback
from io import BytesIO
import stripe

app = Flask(__name__)

# ✅ Stripe Test Key
stripe.api_key = "sk_test_51sfuJ1GXW2HJur5PnDM1nTbr5P96PAUKWdpCe7gjiNzf9Mj3XE6xrWJ91cQpH8oy63y9j7A0yJ1koMSCQyTnCCTbo1h3t4XARLg100kUAsqDKPr"
YOUR_PRICE = 300  # $3.00 in cents

@app.route('/')
def index():
    return '''
    <html>
    <head><title>TaxLabs</title></head>
    <body style="background-color:#0a0a1f; color:white; font-family:sans-serif; text-align:center; padding-top:100px;">
        <h1 style="color:#00bfff;">TaxLabs</h1>
        <p>Upload your wallet CSV.<br>Get clarity in seconds.</p>
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <br><br>
            <button type="submit" style="background:#00bfff; color:white; border:none; padding:10px 20px; cursor:pointer;">Generate Report</button>
        </form>
        <br>
        <a href="/checkout" style="color:#00bfff;">💳 Buy Full Report ($3.00)</a>
    </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        df = pd.read_csv(file)

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

@app.route("/success")
def success():
    return """
    ✅ Payment successful!<br>
    Your PDF is unlocked.<br>
    You can now close this window or go back to the app.
    """

@app.route("/cancel")
def cancel():
    return """
    ❌ Payment was cancelled.<br>
    No charge was made. Please try again if you still want the PDF.
    """

# ✅ PDF generator (basic version)
def generate_pdf(df, buffer):
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(buffer)
    c.drawString(100, 800, "Tax Report Summary")
    y = 750
    for index, row in df.iterrows():
        line = f"{row['date']} | {row['type']} | {row['asset']} | ${row['usd_value']}"
        c.drawString(100, y, line)
        y -= 20
    c.save()

# ✅ Debug run
if __name__ == "__main__":
    app.run(debug=True)
