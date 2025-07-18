import streamlit as st
import pandas as pd
from utils.ocr import extract_text_from_pdf
from utils.classifier import classify_transactions, generate_trial_balance

st.title("AI Bookkeeping SaaS - v2")

st.sidebar.header("Upload")
uploaded_file = st.sidebar.file_uploader("Upload bank statement (PDF)", type=["pdf"])

if uploaded_file:
    st.success("File uploaded!")
    text = extract_text_from_pdf(uploaded_file)
    st.text_area("Extracted Text", text, height=200)

    st.write("Classifying transactions...")
    ledger_df, flagged_df = classify_transactions(text)
    st.subheader("General Ledger")
    st.dataframe(ledger_df)

    if not flagged_df.empty:
        st.subheader("⚠️ Transactions Requiring Human Review")
        st.dataframe(flagged_df)

    st.download_button("Download General Ledger (CSV)", ledger_df.to_csv(index=False), "general_ledger.csv")

    st.subheader("Trial Balance")
    tb_df = generate_trial_balance(ledger_df)
    st.dataframe(tb_df)
    st.download_button("Download Trial Balance (CSV)", tb_df.to_csv(index=False), "trial_balance.csv")
