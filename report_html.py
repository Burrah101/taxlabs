import pandas as pd
from datetime import datetime

def generate_report(csv_path, output_html_path="report.html"):
    df = pd.read_csv(
        csv_path,
        on_bad_lines="skip",
        engine="python"
    )

    df.columns = [c.lower().strip() for c in df.columns]

    total_transactions = len(df)

    counts = df.get("type", pd.Series()).value_counts().to_dict()

    taxable_types = {"sell", "swap", "income"}
    taxable_events = sum(counts.get(t, 0) for t in taxable_types)

    net_usd = int(df.get("usd_value", pd.Series([0])).fillna(0).sum())

    today = datetime.today().strftime("%Y-%m-%d")

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>TaxLabs Report</title></head>
<body>
<h1>TaxLabs — Crypto Tax Checkup</h1>
<p>Generated on {today}</p>
<p>Total transactions: {total_transactions}</p>
<p>Taxable events: {taxable_events}</p>
<p>Estimated net USD activity: ${net_usd}</p>
</body>
</html>
"""

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_html_path
