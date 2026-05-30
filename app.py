import streamlit as st
from SmartApi import SmartConnect
import pyotp
import pandas as pd
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="HeyFund Pro Dashboard", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- LOGIN PAGE ---
def login_page():
    st.markdown("<h1 style='text-align:center; color:#b8922e;'>HeyFund Terminal Login</h1>", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            api_key = st.text_input("AngelOne API Key", type="password")
            client_id = st.text_input("Client ID (e.g. S12345)")
            password = st.text_input("Trading PIN", type="password")
            totp_key = st.text_input("Enter TOTP Key (from App/Authenticator)")
            
            if st.button("🚀 Connect to AngelOne"):
                try:
                    # Logic to connect to AngelOne
                    # obj = SmartConnect(api_key=api_key)
                    # data = obj.generateSession(client_id, password, pyotp.TOTP(totp_key).now())
                    st.session_state.logged_in = True
                    st.success("Connected Successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Login Failed: {e}")

# --- DASHBOARD PAGES ---
def main_dashboard():
    st.sidebar.title("HEYFUND PRO")
    page = st.sidebar.radio("Navigation", ["Stock Analysis", "Option Chain", "Market Movers"])
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if page == "Stock Analysis":
        st.title("📊 HeyFund Stock Analysis")
        # Yahan wahi purana Report wala code aayega
        st.info("Bhai, yahan aapka wahi Sundar Report dikhega.")

    elif page == "Option Chain":
        st.title("⛓️ Nifty & BankNifty Split View")
        # Yahan wahi Split View layout aayega
        st.markdown("### Expiry: 06 JUN 2024")
        col1, col2 = st.columns(2)
        with col1: st.write("NIFTY 50 (Live Table)")
        with col2: st.write("BANK NIFTY (Live Table)")
        st.info("Bhai, jab AngelOne Live hoga, toh yahan data automatic bharega.")

    elif page == "Market Movers":
        st.title("🔥 Market Pulse")
        st.write("Top 10 Gainers / Losers / Volume Shockers")

# --- APP FLOW ---
if not st.session_state.logged_in:
    login_page()
else:
    main_dashboard()
