from flask import Flask, redirect, request, send_file
from dotenv import load_dotenv
import stripe
import os
from report_pdf import create_pdf  # this should return the path to the generated PDF

load_dotenv()

app = Flask(__name__)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.route('/')
def index():
    return '<h1>Welcome to TaxLabs.io</h1><a href="/pay">Pay Now</a>'

@app.route('/pay')
def pay():
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

@app.route('/success')
def success():
    pdf_path = create_pdf()  # Generate PDF after successful payment
    return send_file(pdf_path, as_attachment=True, download_name="Tax_Report.pdf")

@app.route('/cancel')
def cancel():
    return "<h1>Payment cancelled.</h1>"
