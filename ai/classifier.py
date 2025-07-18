
def classify_transactions(df):
    df["AI Category"] = df["Description"].apply(lambda x: "Sales" if "sale" in x.lower() else "Other Income")
    return df
