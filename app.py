from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
from io import BytesIO
import pandas as pd
import traceback
import stripe

app = Flask(__name__)

# ✅ Real Stripe Test Secret Key (working from your Python shell)
stripe.api_key = "sk_test_51SfuJ1GXW2HJur5PrLI492yZpSN5OVbmcJPF4HARJVLCuIcuAFBnDJzWx4ka5UVGzCIJDkElv0vI9XDa2efEpSuN00ECDBsziU"
print(f"🔐 Stripe key in use: {stripe.api_key}")  # Debug print

# ✅ Stripe Checkout Route
@app.route("/checkout")
def checkout():
    try:
        print("⚙️ Creating Stripe Checkout session...")  # Debug print
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "unit_amount": 300,  # $3.00
                    "product_data": {"name": "Tax Report PDF"},
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=url_for('success', _external=True),
            cancel_url=url_for('cancel', _external=True),
        )
        print("✅ Redirecting to Stripe Checkout:", session.url)
        return redirect(session.url, code=303)
    except Exception as e:
        print("❌ Stripe Error:", e)
        return "Something went wrong during checkout.", 500


# ✅ Route for Upload Page
@app.route("/")
def index():
    return render_template("index.html")


# ✅ Route to Handle File Upload and Generate PDF
@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files["file"]
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        df = pd.read_csv(file)

        # Create PDF in-memory
        from reportlab.pdfgen import canvas
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer)
        c.drawString(100, 800, "Tax Report Summary")
        y = 750
        for index, row in df.iterrows():
            line = f"{row['date']} | {row['type']} | {row['asset']} | ${row['usd_value']}"
            c.drawString(100, y, line)
            y -= 20
        c.save()

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


# ✅ Success and Cancel Routes
@app.route("/success")
def success():
    return "✅ Payment successful! You can now download your PDF."


@app.route("/cancel")
def cancel():
    return "❌ Payment was cancelled. Please try again."


# ✅ Optional Debug Test Route
@app.route("/test")
def test():
    return "✅ You are running the correct app.py"


# ✅ Run Locally
if __name__ == "__main__":
    app.run(debug=True)
