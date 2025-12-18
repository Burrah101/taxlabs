import pandas as pd
from datetime import datetime

def generate_report(csv_path, output_html_path="report.html"):
    df = pd.read_csv(
        csv_path,
        on_bad_lines="skip",   # 🔥 CRITICAL FIX
        engine="python"
    )

    df.columns = [c.lower().strip() for c in df.columns]

    total_transactions = len(df)
    counts = df.get("type", pd.Series()).value_counts().to_dict()

    taxable_types = {"sell", "swap", "income"}
    taxable_events = sum(counts.get(t, 0) for t in taxable_types)

    net_usd = int(df.get("usd_value", pd.Series([0])).fillna(0).sum())
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
  max-width:720px;
  margin:auto;
}}
table {{ width:100%; border-collapse:collapse; }}
td, th {{ padding:10px; border-bottom:1px solid #1e293b; }}
.alert {{ margin:20px 0; padding:15px; border-radius:10px; }}
.warning {{ background:#3f2d0c; color:#fde68a; }}
.success {{ background:#052e1a; color:#86efac; }}
</style>
</head>
<body>
<div class="container">

<h1>TaxLabs — Crypto Tax Checkup</h1>
<p>Generated on {today}</p>

<h3>Activity Overview</h3>
<p>Total transactions reviewed: {total_transactions}</p>

<table>
<tr><th>Type</th><th>Count</th></tr>
{''.join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k,v in counts.items())}
</table>

<div class="alert warning">
⚠️ {taxable_events} events are likely taxable.
</div>

<div class="alert success">
💰 Estimated net USD activity: ${net_usd}
</div>

</div>
</body>
</html>
"""

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_html_path
