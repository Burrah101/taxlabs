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
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": "Processing failed", "details": str(e)}), 500
