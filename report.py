from summary import generate_summary

def generate_text_report(csv_path):
    s = generate_summary(csv_path)

    report = f"""
TAXLABS — CRYPTO TAX CHECKUP
--------------------------------

Hey — here’s a quick, plain-English look at your crypto activity.

📊 OVERVIEW
You had {s['total_transactions']} crypto transactions in total.

Here’s how they break down:
"""
    for k, v in s["by_category"].items():
        report += f"  • {k.capitalize()}: {v}\n"

    report += f"""
⚠️ WHAT DESERVES ATTENTION
You have **{s['likely_taxable_events']} transactions that are likely taxable**.
These usually come from sells, swaps, or crypto income.

You also have {s['non_taxable_events']} transactions that are typically not taxable
(like transfers between wallets you control).

💰 BIG PICTURE
Your estimated net USD flow across these transactions is **${s['net_usd_flow']}**.
This helps frame how much activity an accountant or tax tool will care about.

🧭 WHAT TO DO NEXT
• If you’re filing soon, share this summary with your accountant
• If you’re using tax software, this helps you know what to double-check
• If you’re unsure, focus first on sells, swaps, and income events

This isn’t tax advice — it’s clarity.
And clarity saves time, money, and stress.
"""

    return report

if __name__ == "__main__":
    report = generate_text_report("sample.csv")
    print(report)
