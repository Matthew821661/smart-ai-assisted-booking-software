
def classify_transactions(df):
    df['Account'] = df['Description'].apply(lambda x: "Sales" if "sale" in x.lower() else "General Expenses")
    df['VAT Rate'] = 15
    return df
