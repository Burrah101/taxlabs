from flask import Flask, redirect, request, send_file
from dotenv import load_dotenv
import stripe
import os
from report_pdf import generate_pdf  # ✅ Correct function name

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set Stripe secret key from .env
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Home page
@app.route('/')
def index():
    return '''
        <h1>Welcome to TaxLabs.io</h1>
        <p>Get your instant tax report PDF after payment.</p>
        <a href="/pay">Pay Now ($20)</a>
    '''

# Payment route
@app.route('/pay')
def pay():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': 2000,  # $20.00
                    'product_data': {
                        'name': 'Tax Report PDF',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:5000/success',
            cancel_url='http://localhost:5000/cancel',
        )
        return redirect(session.url, code=303)
    except Exception as e:
        return f"❌ Error creating Stripe session: {str(e)}"

# Stripe success route → generate and send PDF
@app.route('/success')
def success():
    try:
        pdf_path = generate_pdf()  # ✅ Now correctly named
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name="Tax_Report.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return f"❌ Failed to generate PDF: {str(e)}"

# Payment cancelled
@app.route('/cancel')
def cancel():
    return "<h2>Payment was cancelled. Please try again.</h2>"

# Run the Flask server locally
if __name__ == "__main__":
    app.run(debug=True)
