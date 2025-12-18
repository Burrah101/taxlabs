def classify_transaction(row):
    t = row["type"].lower()

    if t == "buy":
        return {
            "category": "buy",
            "taxable": False,
            "note": "Buying crypto is usually not a taxable event"
        }

    if t == "sell":
        return {
            "category": "sell",
            "taxable": True,
            "note": "Selling crypto is usually taxable"
        }

    if t == "swap":
        return {
            "category": "swap",
            "taxable": True,
            "note": "Swapping crypto is usually a taxable event"
        }

    if t == "income":
        return {
            "category": "income",
            "taxable": True,
            "note": "Crypto income is usually taxable"
        }

    if t == "transfer":
        return {
            "category": "transfer",
            "taxable": False,
            "note": "Transfers between your own wallets are usually not taxable"
        }

    return {
        "category": "unknown",
        "taxable": False,
        "note": "Unknown transaction type"
    }
