import pandas as pd
from datetime import datetime


def generate_report(csv_path, output_html_path):
    # 🔒 PROD MODE CSV CLEANING
    df = pd.read_csv(
        csv_path,
        sep=",",
        engine="python",
        on_bad_lines="skip",
        skip_blank_lines=True
    )

    df.columns = [c.strip().lower() for c in df.columns]

    required_columns = {"type", "usd_value"}
    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"CSV missing required columns: {missing}")

    total_transactions = len(df)
    counts = df["type"].value_counts().to_dict()

    taxable_types = {"sell", "swap", "income"}
    taxable_events = sum(counts.get(t, 0) for t in taxable_types)

    net_usd = int(df["usd_value"].fillna(0).sum())
    today = datetime.today().strftime("%Y-%m-%d")

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>TaxLabs — Crypto Tax Checkup</title>
<style>
body {{
  background: radial-gradient(circle at top, #0f172a, #020617);
  color: #e5e7eb;
  font-family: system-ui, sans-serif;
  padding: 40px;
}}

.container {{
  max-width: 760px;
  margin: auto;
  background: #020617;
  border-radius: 18px;
  padding: 40px;
}}

h1 {{ color: #38bdf8; }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ padding: 10px; border-bottom: 1px solid #1e293b; }}
.alert {{ margin-top: 20px; padding: 16px; border-radius: 12px; }}
.warning {{ background: #3f2d0c; color: #fde68a; }}
.success {{ background: #052e1a; color: #86efac; }}
</style>
</head>
<body>
<div class="container">
<h1>TaxLabs — Crypto Tax Checkup</h1>
<p>Generated on {today}</p>

<h3>Activity overview</h3>
<p><strong>Total transactions:</strong> {total_transactions}</p>

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

<p style="margin-top:20px;font-size:12px;color:#94a3b8;">
This report is informational only and not tax advice.
</p>

</div>
</body>
</html>
"""

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html)
