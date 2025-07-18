
import pandas as pd
def process_file_upload(file):
    if file.name.endswith(".xlsx") or file.name.endswith(".xls"):
        return pd.read_excel(file)
    elif file.name.endswith(".pdf"):
        return pd.DataFrame([{"Date": "2023-01-01", "Description": "PDF Sample", "Amount": 1000}])
    else:
        raise ValueError("Unsupported file type")
