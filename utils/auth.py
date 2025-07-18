import streamlit_authenticator as stauth
import streamlit as st

def authenticate_user():
    credentials = {
        "usernames": {
            "client1": {"name": "Client 1", "password": "password1"},
            "client2": {"name": "Client 2", "password": "password2"}
        }
    }
    authenticator = stauth.Authenticate(credentials, "auth_cookie", "random_key", cookie_expiry_days=1)
    name, auth_status, username = authenticator.login("Login", "main")
    if auth_status:
        st.sidebar.success(f"Welcome, {name}!")
        return username
    elif auth_status is False:
        st.sidebar.error("Invalid credentials")
    return None
