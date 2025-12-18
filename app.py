from flask import Flask, request, jsonify

app = Flask(__name__)

# Railway-compatible health check
@app.route("/", methods=["GET"])
def root():
    return "OK", 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok"), 200

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    return jsonify({
        "filename": file.filename,
        "status": "received"
    }), 200
