@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return jsonify({"error": "GET not allowed"}), 405

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    email = request.form.get("email", None)

    try:
        html = parse_csv_to_html(file)
        pdf = generate_pdf(html)

        if email:
            send_email_with_attachment(email, pdf)

        return send_file(
            io.BytesIO(pdf),
            as_attachment=True,
            download_name="TaxLabs_Report.pdf",
            mimetype="application/pdf",
        )
    except Exception as e:
        return jsonify({"error": "Processing failed", "details": str(e)}), 500
