
from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def store_ledger(email, ledger_df):
    data = ledger_df.to_dict("records")
    for row in data:
        row['user_email'] = email
    supabase.table("ledgers").insert(data).execute()

def log_upload(email, filename):
    supabase.table("uploads").insert({
        "user_email": email,
        "filename": filename
    }).execute()
