
def generate_ledger_from_ai(ai_data):
    ledger = ai_data.copy()
    ledger["Ledger Account"] = ai_data["AI Category"]
    ledger["Debit"] = ai_data["Amount"].apply(lambda x: x if x > 0 else 0)
    ledger["Credit"] = ai_data["Amount"].apply(lambda x: -x if x < 0 else 0)
    return ledger
