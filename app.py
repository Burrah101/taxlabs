from flask import Flask, request, jsonify
import os

# TEMPORARILY DISABLED TO DEBUG 502
# from report_html import generate_report
# from report_pdf import generate_pdf

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return "TaxLabs backend is running", 200


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    # TEMPORARILY DISABLED TO DEBUG 502
    # generate_report(file)
    # generate_pdf(file)

    return jsonify({
        "filename": file.filename,
        "status": "received"
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
