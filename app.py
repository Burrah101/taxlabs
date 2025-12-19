from flask import Flask, request, send_file, render_template, jsonify
import pandas as pd
from io import BytesIO
import traceback
from report_pdf import generate_pdf  # Ensure this function writes to pdf_buffer

app = Flask(__name__)
import stripe
stripe.api_key = "sk_test_51SfuJ1GXW2HJur5PG9FAUKWdpCe79jlnXMj3XE6xrWJ91cQpH80y6Jy9j7A0yJlkoM5CQyTnC0Tbo1h3t4XRALg100KuASqDKr"  # Replace with your actual key

YOUR_PRICE = 300  # $3.00 in cents
stripe.api_key = "sk_test_51SfuJ1GXW2HJur5PG9FAUKWdpCe79jlnXMj3XE6xrWJ91cQpH80y6Jy9j7A0yJlkoM5CQyTnC0Tbo1h3t4XRALg100KuASqDKr"  # Replace with your actual key

YOUR_PRICE = 300  # $3.00 in cents

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        df = pd.read_csv(file)

        # Create in-memory buffer
        pdf_buffer = BytesIO()
        generate_pdf(df, pdf_buffer)  # This must WRITE into the buffer
        pdf_buffer.seek(0)

        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='TaxLabs_Report.pdf'
        )

    except Exception as e:
        print("===== EXCEPTION START =====")
        print(traceback.format_exc())
        print("===== EXCEPTION END =====")
        return jsonify({"error": "Processing failed", "details": str(e)}), 500

# 🔥 LOCAL DEV SERVER (use only locally)
if __name__ == '__main__':
    app.run(debug=True)
