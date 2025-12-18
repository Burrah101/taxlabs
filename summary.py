from parse_csv import load_csv
from classify import classify_transaction

def generate_summary(csv_path):
    df = load_csv(csv_path)

    classifications = df.apply(classify_transaction, axis=1)
    df["category"] = classifications.apply(lambda x: x["category"])
    df["taxable"] = classifications.apply(lambda x: x["taxable"])

    summary = {
        "total_transactions": len(df),
        "by_category": df["category"].value_counts().to_dict(),
        "likely_taxable_events": int(df["taxable"].sum()),
        "non_taxable_events": int((~df["taxable"]).sum()),
        "net_usd_flow": round(df["usd_value"].sum(), 2)
    }

    return summary

if __name__ == "__main__":
    summary = generate_summary("sample.csv")

    print("\n=== TAXLABS SUMMARY ===")
    for k, v in summary.items():
        print(f"{k}: {v}")
