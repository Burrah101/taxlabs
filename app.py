from flask import Flask, request, send_file, jsonify
from io import BytesIO
import pandas as pd
import traceback
from report_pdf import generate_pdf  # assumes this function exists and is fixed

app = Flask(__name__)

@app.route('/')
def index():
    return 'TaxLabs is running.'

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # 1. Read uploaded CSV
        file = request.files['file']
        df = pd.read_csv(file)

        # 2. Create PDF in memory
        pdf_buffer = BytesIO()
        generate_pdf(df, pdf_buffer)  # <- Must write to pdf_buffer
        pdf_buffer.seek(0)

        # 3. Send PDF file back
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='TaxLabs_Report.pdf'
        )

    except Exception as e:
        print("===== EXCEPTION TRACEBACK =====")
        print(traceback.format_exc())
        return jsonify({
            "error": "Processing failed",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
