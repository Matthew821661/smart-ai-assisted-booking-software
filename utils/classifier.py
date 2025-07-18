import pandas as pd
from datetime import datetime

def classify_transactions(text, doc_type="bank"):
    ledger_entries = []
    flagged_entries = []
    for line in text.split("\n"):
        if any(char.isdigit() for char in line):
            date = datetime.today().strftime("%Y-%m-%d")
            desc = line.strip()
            amount = 1000

            if doc_type == "invoice":
                if "vat" in desc.lower():
                    ledger_entries.append({"Date": date, "Account": "VAT Payable (15%)", "Description": desc, "Debit": 0, "Credit": amount * 0.15})
                elif "zero" in desc.lower():
                    ledger_entries.append({"Date": date, "Account": "VAT Zero-rated", "Description": desc, "Debit": 0, "Credit": 0})
                elif "exempt" in desc.lower():
                    ledger_entries.append({"Date": date, "Account": "VAT Exempt", "Description": desc, "Debit": 0, "Credit": 0})
                else:
                    ledger_entries.append({"Date": date, "Account": "Inventory", "Description": desc, "Debit": amount, "Credit": 0})
                    ledger_entries.append({"Date": date, "Account": "Creditors", "Description": desc, "Debit": 0, "Credit": amount})
            else:
                if "purchase" in desc.lower():
                    ledger_entries.append({"Date": date, "Account": "Inventory", "Description": desc, "Debit": amount, "Credit": 0})
                    ledger_entries.append({"Date": date, "Account": "Creditors", "Description": desc, "Debit": 0, "Credit": amount})
                elif "sale" in desc.lower():
                    ledger_entries.append({"Date": date, "Account": "Debtors", "Description": desc, "Debit": amount, "Credit": 0})
                    ledger_entries.append({"Date": date, "Account": "Sales", "Description": desc, "Debit": 0, "Credit": amount})
                else:
                    flagged_entries.append({"description": desc})
    return pd.DataFrame(ledger_entries), pd.DataFrame(flagged_entries)

def generate_trial_balance(df):
    return df.groupby("Account").agg({"Debit": "sum", "Credit": "sum"}).reset_index()

def calculate_vat(df):
    vat_entries = df[df["Account"].str.contains("VAT", case=False)]
    return vat_entries.groupby("Account").agg({"Debit": "sum", "Credit": "sum"}).reset_index()

def reconcile_bank(df):
    summary = df[df["Account"].str.contains("Cash|Bank", case=False)]
    return summary.groupby("Account").agg({"Debit": "sum", "Credit": "sum"}).reset_index()
