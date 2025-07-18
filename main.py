
# v10 upgrade with GPT-powered 'Explain This Entry'
# Includes AI classification, ledger generation, and GPT explanations

import streamlit as st
import pandas as pd
from utils.ledger import generate_ledger_from_ai
from utils.upload import process_file_upload
from ai.classifier import classify_transactions
from database.supabase_io import log_upload, store_ledger
from utils.gpt_explainer import explain_entry

st.set_page_config(page_title="AI Bookkeeping Upload", layout="wide")
st.title("📤 Upload Bank Statements or Invoices")

uploaded_file = st.file_uploader("Upload PDF or Excel file", type=["pdf", "xlsx", "xls"])

if uploaded_file:
    st.success("✅ File uploaded successfully")

    # Step 1: Process File
    try:
        df_transactions = process_file_upload(uploaded_file)
        st.write("### Extracted Transactions")
        st.dataframe(df_transactions)
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        st.stop()

    # Step 2: Classify
    st.write("### 🤖 AI Classification")
    try:
        ai_output = classify_transactions(df_transactions)
        st.dataframe(ai_output)
    except Exception as e:
        st.error(f"❌ AI classification error: {e}")
        st.stop()

    # Step 3: Generate Ledger
    st.write("### 📘 Generated General Ledger")
    ledger = generate_ledger_from_ai(ai_output)
    st.dataframe(ledger)

    # Step 3.5: Explain Entry (GPT)
    st.write("### 💬 GPT Explain This Entry")
    selected_row = st.selectbox("Select a transaction to explain", ledger.index)
    if selected_row is not None:
        entry = ledger.loc[selected_row].to_dict()
        if st.button("Explain This Entry"):
            explanation = explain_entry(entry)
            st.info(explanation)

    # Step 4: Store to Supabase
    if st.button("Save to Client Ledger"):
        try:
            user_email = st.session_state.get("user_email", "test@example.com")
            store_ledger(user_email, ledger)
            log_upload(user_email, uploaded_file.name)
            st.success("✅ Ledger stored successfully!")
        except Exception as e:
            st.error(f"Error saving to Supabase: {e}")
