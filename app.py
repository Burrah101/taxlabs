from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from report_html import generate_report
from report_pdf import generate_pdf

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    generate_report(path)
    generate_pdf(path)

    return send_file("report.pdf", as_attachment=True)

@app.route("/")
def health():
    return "TaxLabs backend running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
