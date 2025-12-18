from flask import Flask, request, jsonify
import os

# Report generation
from report_html import generate_report
from report_pdf import generate_pdf

app = Flask(__name__)

UPLOAD_DIR = "uploads"


@app.route("/", methods=["GET"])
def health():
    return "TaxLabs backend is running", 200


@app.route("/upload", methods=["POST"])
def upload():
    # Validate upload
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    if not file.filename.lower().endswith(".csv"):
        return jsonify({"error": "Only CSV files are allowed"}), 400

    # Save file
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(path)

    # Generate reports
    try:
        generate_report(path)
        generate_pdf(path)
    except Exception as e:
        # CRITICAL: return real error instead of crashing
        return jsonify({
            "error": "Report generation failed",
            "details": str(e)
        }), 500

    return jsonify({
        "status": "success",
        "file": file.filename
    }), 200
