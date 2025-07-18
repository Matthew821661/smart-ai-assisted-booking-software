import streamlit as st
import pandas as pd
from utils.ocr import extract_text_from_pdf
from utils.classifier import classify_transactions, generate_trial_balance, calculate_vat, reconcile_bank
from utils.db import insert_gl_entries, log_upload
from utils.exporter import export_pdf_report
from utils.supabase_auth import login_user, upload_to_supabase, list_uploaded_files

st.set_page_config(page_title="AI Bookkeeping SaaS v5", layout="wide")
st.title("AI Bookkeeping SaaS - v5 (Supabase Login + Cloud Storage)")

# --- User Login ---
user_email = login_user()
if not user_email:
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
        st.subheader("⚠️ Flagged Transactions")
        st.dataframe(flagged_df)

    st.subheader("📊 Trial Balance")
    tb_df = generate_trial_balance(ledger_df)
    st.dataframe(tb_df)

    st.subheader("💰 VAT Summary")
    vat_df = calculate_vat(ledger_df)
    st.dataframe(vat_df)

    st.subheader("🔄 Bank Reconciliation")
    rec_df = reconcile_bank(ledger_df)
    st.dataframe(rec_df)

    # Store file in Supabase
    if st.button("📤 Upload Ledger to Cloud"):
        upload_to_supabase(user_email, ledger_df)
        insert_gl_entries(user_email, ledger_df)
        log_upload(user_email, 'ledger.csv')

    # Report downloads
    st.download_button("Download GL (CSV)", ledger_df.to_csv(index=False), "general_ledger.csv")
    st.download_button("Download TB (CSV)", tb_df.to_csv(index=False), "trial_balance.csv")
    st.download_button("Download VAT (CSV)", vat_df.to_csv(index=False), "vat_summary.csv")

    if st.button("📥 PDF Financial Report"):
        pdf_path = export_pdf_report(ledger_df, tb_df, vat_df)
        with open(pdf_path, "rb") as f:
            st.download_button("Download Report", f, "financial_report.pdf")

# List historical uploads
st.sidebar.subheader("📂 Upload History")
files = list_uploaded_files(user_email)
st.sidebar.write(files)
