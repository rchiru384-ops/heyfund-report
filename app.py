import streamlit as st
from SmartApi import SmartConnect
import pyotp
import pandas as pd
import datetime
import time

# --- CONFIG ---
st.set_page_config(page_title="HeyFund Live Terminal", layout="wide")

# CSS for the EXACT Image Look
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    body { background-color: #f0f2f5; font-family: 'DM Sans', sans-serif; }
    .stApp { background-color: #f0f2f5; }
    .sidebar-content { background-color: #111118 !important; }
    .report-card { background: white; border-radius: 12px; padding: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px; border: 1px solid #e0e0e0; }
    .gold-text { color: #b8922e; font-weight: bold; }
    .metric-val { font-size: 24px; font-weight: bold; color: #111; }
    </style>
""", unsafe_allow_html=True)

# --- CREDENTIALS ---
API_KEY = "OiFQFiQV"
CLIENT_ID = "R62843391"
MPIN = "0619"
TOTP_SECRET = "YAB6GB2JRC3WVGJR7ZKQYGCK6I"

if 'angel' not in st.session_state:
    st.session_state.angel = None

# --- ANGELONE CONNECTION ---
def connect():
    try:
        obj = SmartConnect(api_key=API_KEY)
        token = pyotp.TOTP(TOTP_SECRET).now()
        data = obj.generateSession(CLIENT_ID, MPIN, token)
        if data['status']: return obj
        return None
    except: return None

# --- DASHBOARD PAGE ---
def render_dashboard(obj):
    # Fetching Real-Time Prices
    try:
        # 2885 = Reliance, 99926000 = Nifty
        res = obj.getLTP("NSE", "RELIANCE-EQ", "2885")
        rel_price = res['data']['ltp'] if res['status'] else 2950.00
        nifty_res = obj.getLTP("NSE", "Nifty 50", "99926000")
        nifty_price = nifty_res['data']['ltp'] if nifty_res['status'] else 22510.00
    except:
        rel_price, nifty_price = 2950.00, 22510.00

    # UI Header (Matches Image)
    st.markdown(f"""
    <div class="report-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div style="font-size:12px; color:#b8922e; font-weight:bold;">STOCK RISK REPORT</div>
                <h2 style="margin:0;">RELIANCE INDUSTRIES LTD (NSE: RELIANCE)</h2>
            </div>
            <div style="text-align:right;">
                <div style="font-size:28px; font-weight:bold;">₹{rel_price:,.2f} <span style="color:#15803d; font-size:16px;">+12.45 (0.52%)</span></div>
                <div style="font-size:11px; color:#666;">As of {datetime.datetime.now().strftime('%H:%M:%S')} IST</div>
            </div>
        </div>
        <hr style="border:0.5px solid #eee; margin:20px 0;">
        <div style="display:flex; align-items:center;">
            <div style="flex:1; text-align:center;">
                <svg width="250" height="140" viewBox="0 0 300 180">
                    <path d="M 40 150 A 110 110 0 0 1 260 150" fill="none" stroke="#eee" stroke-width="20" stroke-linecap="round"/>
                    <path d="M 40 150 A 110 110 0 0 1 180 50" fill="none" stroke="#f1c40f" stroke-width="20" stroke-linecap="round"/>
                    <line x1="150" y1="150" x2="180" y2="70" stroke="#333" stroke-width="4" stroke-linecap="round"/>
                    <circle cx="150" cy="150" r="5" fill="#333"/>
                </svg>
                <div style="margin-top:-40px; font-weight:bold; color:#b8922e;">MODERATE RISK</div>
                <div style="font-size:11px; color:#666;">Risk Score: 5.4/10</div>
            </div>
            <div style="flex:1; display:grid; grid-template-columns:1fr 1fr; gap:15px; font-size:13px;">
                <div>Volatility<br><b>Medium (42.1%)</b></div>
                <div>Correlation<br><b>Neutral (0.65)</b></div>
                <div>Market Sentiment<br><b>Neutral</b></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Option Chain (Matches Image Table)
    st.markdown(f"""
    <div class="report-card">
        <div style="font-size:14px; font-weight:bold; color:#b8922e; margin-bottom:15px;">NIFTY OPTION CHAIN PREVIEW (SPOT: ₹{nifty_price:,.2f})</div>
        <table style="width:100%; text-align:center; font-size:11px; border-collapse:collapse;">
            <tr style="background:#fdf9f0; font-weight:bold;">
                <td colspan="4" style="padding:10px;">Call Options</td>
                <td style="background:#fceecb;">Strike Price</td>
                <td colspan="4">Put Options</td>
            </tr>
            <tr style="font-size:10px; color:#666; background:#fafafa;">
                <th>OI</th><th>LTP</th><th>IV</th><th>Delta</th>
                <th style="background:#fceecb; color:black;">Center</th>
                <th>Delta</th><th>IV</th><th>LTP</th><th>OI</th>
            </tr>
            <tr><td>3.0L</td><td>125.4</td><td>30.8%</td><td>0.65</td><td style="background:#fceecb; font-weight:bold;">22400</td><td>0.35</td><td>42%</td><td>42.1</td><td>9.0L</td></tr>
            <tr style="background:#fff7e6; border:1.5px solid #b8922e;"><td>2.3L</td><td>85.2</td><td>100%</td><td>0.50</td><td style="background:#b8922e; color:white; font-weight:bold;">22500</td><td>0.50</td><td>105%</td><td>112.4</td><td>10.3L</td></tr>
            <tr><td>2.0L</td><td>42.1</td><td>97%</td><td>0.35</td><td style="background:#fceecb; font-weight:bold;">22600</td><td>0.65</td><td>76%</td><td>185.2</td><td>7.0L</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-Refresh Script
    time.sleep(2)
    st.rerun()

# --- APP FLOW ---
if st.session_state.angel is None:
    st.markdown("<h1 style='text-align:center; color:#b8922e;'>HEYFUND PRO LOGIN</h1>", unsafe_allow_html=True)
    if st.button("🚀 CONNECT LIVE ANGELONE"):
        session = connect()
        if session:
            st.session_state.angel = session
            st.rerun()
        else: st.error("Check Details!")
else:
    with st.sidebar:
        st.markdown("<h2 style='color:#b8922e;'>HEYFUND</h2>", unsafe_allow_html=True)
        st.radio("MENU", ["Dashboard", "Portfolio", "Research", "Option Chain"])
        if st.button("Logout"):
            st.session_state.angel = None
            st.rerun()
    render_dashboard(st.session_state.angel)
