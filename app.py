from flask import Flask, request, send_file, jsonify, redirect, url_for
import pandas as pd
from io import BytesIO
import traceback

# PDF
from reportlab.pdfgen import canvas

# Stripe
import stripe

app = Flask(__name__)

# =========================
# STRIPE CONFIG (TEST MODE)
# =========================
stripe.api_key = "sk_test_51sfuJ1GXW2HJur5PnDM1nTbr5P96PAUKWdpCe7gjiNzf9Mj3XE6xrWJ91cQpH8oy63y9j7A0yJ1koMSCQyTnCCTbo1h3t4XARLg100kUAsqDKPr"
YOUR_PRICE = 300  # $3.00 in cents


# =========================
# PDF GENERATION
# =========================
def generate_pdf(df, buffer):
    c = canvas.Canvas(buffer)
    c.drawString(100, 800, "TaxLabs — Crypto Tax Report")

    y = 760
    for _, row in df.iterrows():
        line = f"{row['date']} | {row['type']} | {row['asset']} | ${row['usd_value']}"
        c.drawString(80, y, line)
        y -= 18

        if y < 50:
            c.showPage()
            y = 760

    c.save()  # MUST close PDF


# =========================
# ROUTES
# =========================

@app.route("/")
def index():
    return """
    <h2>TaxLabs Local Test</h2>
    <form action="/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="file" accept=".csv" required><br><br>
        <button type="submit">Upload CSV → Download PDF</button>
    </form>
    <br>
    <a href="/checkout">Pay $3 (Stripe Test)</a>
    """


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
            mimetype="application/pdf",
            as_attachment=True,
            download_name="TaxLabs_Report.pdf"
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
            success_url=url_for("success", _external=True),
            cancel_url=url_for("cancel", _external=True),
        )
        return redirect(session.url, code=303)

    except Exception as e:
        print("Stripe error:", e)
        return "Stripe checkout failed", 500


@app.route("/success")
def success():
    return "<h2>✅ Payment successful</h2><p>You may return to the app.</p>"


@app.route("/cancel")
def cancel():
    return "<h2>❌ Payment cancelled</h2>"


# =========================
# LOCAL DEV ENTRYPOINT
# =========================
if __name__ == "__main__":
    app.run(debug=True)
