from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_gl_entries(user_email, df):
    rows = df.to_dict(orient="records")
    for row in rows:
        data = {
            "user_email": user_email,
            "date": row.get("Date"),
            "account": row.get("Account"),
            "description": row.get("Description"),
            "debit": float(row.get("Debit", 0) or 0),
            "credit": float(row.get("Credit", 0) or 0)
        }
        supabase.table("gl_entries").insert(data).execute()

def log_upload(user_email, filename):
    supabase.table("upload_log").insert({
        "user_email": user_email,
        "filename": filename
    }).execute()
