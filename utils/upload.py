
import pandas as pd

def process_file_upload(uploaded_file):
    if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
        return pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith('.pdf'):
        raise NotImplementedError("PDF parsing is not implemented yet.")
    else:
        raise ValueError("Unsupported file type")
