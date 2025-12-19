from flask import Flask, request, jsonify, send_file, render_template, redirect, url_for
import pandas as pd
from io import BytesIO
import stripe
import traceback

app = Flask(__name__)

# ✅ Stripe Secret Key (Make sure this is a valid key — update if rotated)
stripe.api_key = "sk_test_51SfuJ1GXW2HJur5PrLI492yZpSN5OVbmcJPF4HARJVLCuIcuAFBnDJzWx4ka5UVGzCIJDkElv0vI9XDa2efEpSuN00ECDBsziU"
YOUR_PRICE = 300  # $3.00 in cents

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files["file"]
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

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
        print("❌ Upload Error:", traceback.format_exc())
        return jsonify({"error": "Processing failed", "details": str(e)}), 500

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
            success_url=url_for('success', _external=True),
            cancel_url=url_for('cancel', _external=True),
        )
        print("✅ Stripe session created.")
        return redirect(session.url, code=303)

    except Exception as e:
        print("❌ Stripe Error:", traceback.format_exc())
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

if __name__ == "__main__":
    print("✅ This is the correct app.py")
    app.run(debug=True)
