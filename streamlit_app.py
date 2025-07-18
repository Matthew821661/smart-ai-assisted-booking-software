import streamlit as st
import pandas as pd
from utils.ocr import extract_text_from_pdf
from utils.classifier import classify_transactions, generate_trial_balance, calculate_vat, reconcile_bank
from utils.exporter import export_pdf_report
from utils.auth import authenticate_user

st.set_page_config(page_title="AI Bookkeeping SaaS v4", layout="wide")
st.title("AI Bookkeeping SaaS - v4 (Multi-Client, VAT, Reconciliation)")

# --- Login ---
user = authenticate_user()
if not user:
    st.stop()

st.sidebar.header("Upload Documents")
doc_type = st.sidebar.selectbox("Document Type", ["Bank Statement", "Invoice"])
uploaded_file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    st.success("File uploaded!")
    text = extract_text_from_pdf(uploaded_file)
    st.text_area("Extracted Text", text, height=200)

    st.write("🔍 Classifying Transactions...")
    ledger_df, flagged_df = classify_transactions(text, doc_type=doc_type)

    st.subheader("📘 General Ledger")
    st.dataframe(ledger_df)

    if not flagged_df.empty:
        st.subheader("⚠️ Flagged Transactions for Human Review")
        st.dataframe(flagged_df)

    st.subheader("📊 Trial Balance")
    tb_df = generate_trial_balance(ledger_df)
    st.dataframe(tb_df)

    st.subheader("💰 VAT Summary")
    vat_df = calculate_vat(ledger_df)
    st.dataframe(vat_df)

    st.subheader("🔗 Bank Reconciliation")
    reconciliation = reconcile_bank(ledger_df)
    st.dataframe(reconciliation)

    st.download_button("📥 Download General Ledger (CSV)", ledger_df.to_csv(index=False), "general_ledger.csv")
    st.download_button("📥 Download Trial Balance (CSV)", tb_df.to_csv(index=False), "trial_balance.csv")
    st.download_button("📥 Download VAT Summary (CSV)", vat_df.to_csv(index=False), "vat_summary.csv")

    if st.button("📥 Download Full PDF Report"):
        pdf_path = export_pdf_report(ledger_df, tb_df, vat_df)
        with open(pdf_path, "rb") as file:
            st.download_button("Download PDF Report", file, "financial_report.pdf")
