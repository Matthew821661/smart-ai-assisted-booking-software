import streamlit as st
from supabase import create_client
import os
import pandas as pd
from io import StringIO
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def login_user():
    st.sidebar.header("Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.sidebar.success("Logged in!")
            return email
        except Exception as e:
            st.sidebar.error("Login failed")
    return None

def upload_to_supabase(user_email, df):
    csv = df.to_csv(index=False)
    filename = f"{user_email.replace('@','_').replace('.','_')}/ledger_{pd.Timestamp.now().date()}.csv"
    supabase.storage.from_("ledgers").upload(filename, StringIO(csv), {"content-type": "text/csv"})
    st.success("Uploaded to Supabase storage.")

def list_uploaded_files(user_email):
    folder = user_email.replace('@','_').replace('.','_')
    try:
        files = supabase.storage.from_("ledgers").list(folder)
        return [f['name'] for f in files]
    except Exception:
        return ["No files found."]
