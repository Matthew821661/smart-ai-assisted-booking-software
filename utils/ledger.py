
def generate_ledger_from_ai(df):
    ledger = df[['Date', 'Description', 'Amount', 'Account', 'VAT Rate']].copy()
    ledger['Debit'] = ledger['Amount'].apply(lambda x: x if x > 0 else 0)
    ledger['Credit'] = ledger['Amount'].apply(lambda x: -x if x < 0 else 0)
    return ledger
