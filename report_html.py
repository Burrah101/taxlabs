import pandas as pd
from datetime import datetime

def generate_report(csv_path, output_html_path):
    # Read CSV safely (handles broken exchange CSVs)
    df = pd.read_csv(
        csv_path,
        engine="python",
        sep=None,
        on_bad_lines="skip"
    )

    df.columns = [c.lower().strip() for c in df.columns]

    total_transactions = len(df)

    if "type" in df.columns:
        counts = df["type"].value_counts().to_dict()
    else:
        counts = {}

    taxable_types = {"sell", "swap", "income"}
    taxable_events = sum(counts.get(t, 0) for t in taxable_types)

    if "usd_value" in df.columns:
        net_usd = int(pd.to_numeric(df["usd_value"], errors="coerce").fillna(0).sum())
    else:
        net_usd = 0

    today = datetime.today().strftime("%Y-%m-%d")

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>TaxLabs — Crypto Tax Checkup</title>
<style>
body {{
  background:#020617;
  color:#e5e7eb;
  font-family:system-ui;
  padding:40px;
}}
.container {{
  max-width:700px;
  margin:auto;
  background:#0b1220;
  padding:40px;
  border-radius:16px;
}}
h1 {{ color:#38bdf8; }}
table {{ width:100%; margin-top:20px; border-collapse:collapse; }}
td, th {{ padding:8px; border-bottom:1px solid #1e293b; }}
.alert {{ margin-top:20px; padding:14px; border-radius:10px; }}
.warning {{ background:#3f2d0c; color:#fde68a; }}
.success {{ background:#052e1a; color:#86efac; }}
</style>
</head>
<body>
<div class="container">
<h1>TaxLabs — Crypto Tax Checkup</h1>
<p>Generated on {today}</p>

<p><strong>Total transactions reviewed:</strong> {total_transactions}</p>

<table>
<tr><th>Type</th><th>Count</th></tr>
<tr><td>Buy</td><td>{counts.get("buy",0)}</td></tr>
<tr><td>Sell</td><td>{counts.get("sell",0)}</td></tr>
<tr><td>Swap</td><td>{counts.get("swap",0)}</td></tr>
<tr><td>Income</td><td>{counts.get("income",0)}</td></tr>
<tr><td>Transfer</td><td>{counts.get("transfer",0)}</td></tr>
</table>

<div class="alert warning">
⚠️ {taxable_events} events are likely taxable.
</div>

<div class="alert success">
💰 Estimated net USD activity: ${net_usd}
</div>

<p style="margin-top:30px;font-size:0.8rem;color:#94a3b8">
This report is informational only and not tax advice.
</p>

</div>
</body>
</html>
"""

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html)
