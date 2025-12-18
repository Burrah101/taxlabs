from flask import Flask, render_template_string, request, send_file
import os
from report_html import generate_report
from report_pdf import generate_pdf  # your existing PDF script

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

UPLOAD_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>TaxLabs — Upload CSV</title>
  <style>
    body {
      background:#020617;
      color:#e5e7eb;
      font-family: system-ui, sans-serif;
      display:flex;
      align-items:center;
      justify-content:center;
      height:100vh;
    }
    .box {
      background:#0b1220;
      padding:40px;
      border-radius:14px;
      width:420px;
      text-align:center;
      box-shadow:0 20px 60px rgba(0,0,0,.6);
    }
    h1 { color:#38bdf8; }
    input, button {
      margin-top:20px;
      width:100%;
      padding:12px;
      border-radius:8px;
      border:none;
    }
    button {
      background:#38bdf8;
      color:#020617;
      font-weight:700;
      cursor:pointer;
    }
  </style>
</head>
<body>
  <form class="box" method="post" enctype="multipart/form-data">
    <h1>TaxLabs</h1>
    <p>Upload your wallet CSV.<br>Get clarity in seconds.</p>
    <input type="file" name="csv" required>
    <button type="submit">Generate Report</button>
  </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["csv"]
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        generate_report(path)
        generate_pdf(path)

        return send_file("report.pdf", as_attachment=True)

    return render_template_string(UPLOAD_PAGE)

if __name__ == "__main__":
    app.run(debug=True)
