from flask import Flask, request, jsonify

app = Flask(__name__)

# Railway health check (MUST respond fast)
@app.route("/", methods=["GET"])
def health():
    return "TaxLabs backend is running", 200

# Upload endpoint (stub for now)
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    return jsonify({
        "filename": file.filename,
        "status": "received"
    }), 200
