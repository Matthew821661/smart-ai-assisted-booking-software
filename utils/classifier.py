import pandas as pd
from datetime import datetime

def classify_transactions(text):
    ledger_entries = []
    flagged_entries = []
    for line in text.split("\n"):
        if any(char.isdigit() for char in line):
            date = datetime.today().strftime("%Y-%m-%d")
            desc = line.strip()
            amount = 1000  # Placeholder
            if "purchase" in desc.lower():
                ledger_entries.append({"Date": date, "Account": "Inventory", "Description": desc, "Debit": amount, "Credit": 0})
                ledger_entries.append({"Date": date, "Account": "Creditors", "Description": desc, "Debit": 0, "Credit": amount})
            elif "sale" in desc.lower():
                ledger_entries.append({"Date": date, "Account": "Debtors", "Description": desc, "Debit": amount, "Credit": 0})
                ledger_entries.append({"Date": date, "Account": "Sales", "Description": desc, "Debit": 0, "Credit": amount})
            elif "vat" in desc.lower():
                ledger_entries.append({"Date": date, "Account": "VAT Payable", "Description": desc, "Debit": 0, "Credit": amount})
            else:
                # Unsure classification - requires human review
                flagged_entries.append({"description": desc})
    return pd.DataFrame(ledger_entries), pd.DataFrame(flagged_entries)

def generate_trial_balance(df):
    tb = df.groupby("Account").agg({"Debit": "sum", "Credit": "sum"}).reset_index()
    return tb
