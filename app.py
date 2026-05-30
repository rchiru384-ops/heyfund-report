import streamlit as st
from SmartApi import SmartConnect
import pyotp
import pandas as pd
import datetime
import requests

# --- PAGE CONFIG ---
st.set_page_config(page_title="HeyFund Dashboard | Live Terminal", layout="wide")

# --- CUSTOM CSS (IMAGE STYLE) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    body { background-color: #f4f7f9; }
    .report-card { background: white; border-radius: 15px; padding: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .sidebar-nav { background: #111118; color: white; height: 100vh; padding: 20px; }
    .gold-text { color: #b8922e; }
    </style>
""", unsafe_allow_html=True)

# --- ANGELONE CREDENTIALS ---
API_KEY = "OiFQFiQV"
CLIENT_ID = "R62843391"
MPIN = "0619"
TOTP_SECRET = "YAB6GB2JRC3WVGJR7ZKQYGCK6I"

if 'angel' not in st.session_state:
    st.session_state.angel = None

def get_session():
    try:
        obj = SmartConnect(api_key=API_KEY)
        token = pyotp.TOTP(TOTP_SECRET).now()
        data = obj.generateSession(CLIENT_ID, MPIN, token)
        if data['status']: return obj
        return None
    except: return None

def get_ltp(obj, symbol, token, exchange="NSE"):
    try:
        res = obj.getLTP(exchange, symbol, token)
        return res['data']['ltp'] if res['status'] else 0
    except: return 0

# --- MAIN DASHBOARD VIEW ---
def show_dashboard(obj):
    # Fetch Live Data
    nifty_price = get_ltp(obj, "Nifty 50", "99926000")
    # For Demo, let's say we are looking at RELIANCE (Token 2885)
    stock_price = get_ltp(obj, "RELIANCE-EQ", "2885")
    
    # 1. HEADER SECTION (Matches Image)
    st.markdown(f"""
    <div class="report-card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
                <div style="font-size:12px; font-weight:bold; color:#b8922e; margin-bottom:5px;">STOCK RISK REPORT</div>
                <h2 style="margin:0; font-family:sans-serif;">RELIANCE INDUSTRIES LTD (NSE: RELIANCE)</h2>
            </div>
            <div style="text-align:right;">
                <div style="font-size:24px; font-weight:bold;">₹{stock_price:,.2f} <span style="color:#15803d; font-size:14px;">+12.45 (+0.52%)</span></div>
                <div style="font-size:11px; color:#666;">As of {datetime.datetime.now().strftime('%b %d, %Y, %H:%M %p')} IST</div>
            </div>
        </div>
        
        <div style="display:flex; margin-top:30px; align-items:center; gap:50px;">
            <!-- GAUGE (SVG) -->
            <div style="flex:1; text-align:center;">
                <svg width="300" height="180" viewBox="0 0 300 180">
                    <path d="M 40 150 A 110 110 0 0 1 260 150" fill="none" stroke="#eee" stroke-width="25" stroke-linecap="round"/>
                    <path d="M 40 150 A 110 110 0 0 1 150 40" fill="none" stroke="#f1c40f" stroke-width="25" />
                    <line x1="150" y1="150" x2="150" y2="50" stroke="#333" stroke-width="4" stroke-linecap="round"/>
                    <circle cx="150" cy="150" r="6" fill="#333"/>
                </svg>
                <div style="margin-top:-60px;">
                    <div style="font-size:18px; font-weight:bold; color:#b8922e;">MODERATE RISK</div>
                    <div style="font-size:12px; color:#666;">Risk Score: 5.4/10</div>
                </div>
            </div>
            
            <!-- METRICS SIDEBAR -->
            <div style="flex:1; display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
                <div><div style="font-size:11px; color:#666;">Volatility</div><div style="font-weight:bold;">Medium</div></div>
                <div><div style="font-size:11px; color:#666;">Value</div><div style="font-weight:bold;">42.1%</div></div>
                <div><div style="font-size:11px; color:#666;">Correlation</div><div style="font-weight:bold;">Neutral</div></div>
                <div><div style="font-size:11px; color:#666;">Score</div><div style="font-weight:bold;">0.65</div></div>
                <div><div style="font-size:11px; color:#666;">Market Sentiment</div><div style="font-weight:bold;">Neutral</div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. OPTION CHAIN PREVIEW (Matches Image Table)
    st.markdown(f"""
    <div class="report-card">
        <div style="font-size:14px; font-weight:bold; color:#b8922e; margin-bottom:15px;">NIFTY OPTION CHAIN PREVIEW (SPOT: ₹{nifty_price:,.2f})</div>
        <table style="width:100%; border-collapse:collapse; text-align:center; font-size:11px; font-family:sans-serif;">
            <tr style="background:#fdf9f0; font-weight:bold;">
                <td colspan="7">Call Options</td>
                <td style="background:#fceecb;">Strike Price</td>
                <td colspan="7">Put Options</td>
            </tr>
            <tr style="background:#f9f9f9; color:#666; font-size:10px;">
                <th>OI (Lac)</th><th>Chg OI</th><th>Vol (L)</th><th>IV</th><th>LTP</th><th>Bid</th><th>Ask</th>
                <th style="background:#fceecb; color:black;">Center</th>
                <th>Ask</th><th>Bid</th><th>LTP</th><th>IV</th><th>Vol (L)</th><th>Chg OI</th><th>OI (Lac)</th>
            </tr>
            <!-- ATM ROW EXAMPLE -->
            <tr><td>3.0</td><td>+39</td><td>200</td><td>95.8%</td><td>98.6</td><td>38.3</td><td>18.3</td><td style="background:#fceecb; font-weight:bold;">19100</td><td>14.3</td><td>13.3</td><td>98.6</td><td>93.8%</td><td>120</td><td>0</td><td>3.0</td></tr>
            <tr style="background:#fff7e6; border:1.5px solid #b8922e;"><td>2.3</td><td>+15</td><td>160</td><td>100.7%</td><td>125.4</td><td>18.8</td><td>15.3</td><td style="background:#b8922e; color:white; font-weight:bold;">19300</td><td>18.3</td><td>18.8</td><td>75.2</td><td>105.7%</td><td>200</td><td>-14</td><td>10.3</td></tr>
            <tr><td>2.0</td><td>-136</td><td>120</td><td>97.8%</td><td>98.6</td><td>14.3</td><td>18.8</td><td style="background:#fceecb; font-weight:bold;">19400</td><td>16.8</td><td>15.8</td><td>75.3</td><td>76.3%</td><td>120</td><td>-158</td><td>7.0</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

# --- LOGIN FLOW ---
if st.session_state.angel is None:
    st.markdown("<h1 style='text-align:center; color:#b8922e;'>HEYFUND PRO LOGIN</h1>", unsafe_allow_html=True)
    if st.button("🚀 CONNECT LIVE TO ANGELONE"):
        with st.spinner("Logging into SmartAPI..."):
            session = get_session()
            if session:
                st.session_state.angel = session
                st.rerun()
            else: st.error("Login Failed!")
else:
    # SIDEBAR NAVIGATION (Matches Image Icons)
    with st.sidebar:
        st.markdown("<h1 style='color:#b8922e;'>HEYFUND</h1>", unsafe_allow_html=True)
        st.radio("Menu", ["Dashboard", "Portfolio", "Stock Research", "Nifty Option Chain", "Market Insights"])
        if st.button("Logout"):
            st.session_state.angel = None
            st.rerun()
    
    show_dashboard(st.session_state.angel)
