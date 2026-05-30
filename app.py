import streamlit as st
from SmartApi import SmartConnect
import pyotp
import pandas as pd
import datetime
import requests
import time

# --- PAGE SETUP ---
st.set_page_config(page_title="HeyFund Pro Terminal | Live AngelOne", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;700&family=IBM+Plex+Mono&display=swap');
    .metric-card { background: #111118; padding: 15px; border-radius: 10px; border-top: 3px solid #b8922e; text-align: center; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- ANGELONE CREDENTIALS (SAVED) ---
API_KEY = "OiFQFiQV"
CLIENT_ID = "R62843391"
MPIN = "0619"
TOTP_SECRET = "YAB6GB2JRC3WVGJR7ZKQYGCK6I"

if 'angel' not in st.session_state:
    st.session_state.angel = None

# --- LOGIN LOGIC ---
def connect_angelone():
    try:
        smart_api = SmartConnect(api_key=API_KEY)
        totp = pyotp.TOTP(TOTP_SECRET).now()
        data = smart_api.generateSession(CLIENT_ID, MPIN, totp)
        if data['status']:
            st.session_state.angel = smart_api
            return True
        return False
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return False

# --- UI COMPONENTS ---
def show_header(title):
    st.markdown(f"""
        <div style="background:#111118; color:#fff; padding:15px 30px; display:flex; justify-content:space-between; align-items:center; border-radius:10px; margin-bottom:20px;">
            <div><span style="color:#b8922e; font-weight:bold; font-size:22px; font-family:'DM Serif Display';">HeyFund Research Team</span><br><span style="font-size:10px; opacity:0.7;">Live AngelOne Terminal</span></div>
            <div style="text-align:right;"><h3 style="margin:0; color:#b8922e;">{title}</h3></div>
        </div>
    """, unsafe_allow_html=True)

# --- 1. OPTION CHAIN (SPLIT VIEW) ---
def page_option_chain():
    show_header("NIFTY & BANKNIFTY SPLIT VIEW")
    st.sidebar.selectbox("Expiry Date", ["06-JUN-2024", "13-JUN-2024"])
    
    col_l, col_r = st.columns(2)
    
    oc_html = """
    <div style="background:#111118; padding:15px; border-radius:10px; border:1px solid #333; font-family:sans-serif;">
        <div style="display:flex; justify-content:space-between; color:#b8922e; font-weight:bold; margin-bottom:10px;">
            <span>{NAME}</span><span style="color:#00ff88;">SPOT: {SPOT}</span>
        </div>
        <table style="width:100%; color:white; border-collapse:collapse; font-size:11px; text-align:center;">
            <tr style="background:#222; color:#b8922e;"><th>OI</th><th>LTP</th><th style="background:#b8922e; color:black;">STRIKE</th><th>LTP</th><th>OI</th></tr>
            <tr><td>45.2L</td><td>125.4</td><td style="color:#b8922e; background:#1a1a2e;">22400</td><td>42.1</td><td>12.5L</td></tr>
            <tr style="background:#1a1a24; border:1px solid #b8922e;"><td>68.1L</td><td>88.2</td><td style="background:#b8922e; color:black; font-weight:bold;">22500</td><td>112.4</td><td>55.2L</td></tr>
            <tr><td>12.4L</td><td>42.1</td><td style="color:#b8922e; background:#1a1a2e;">22600</td><td>185.2</td><td>92.1L</td></tr>
        </table>
    </div>
    """
    with col_l: st.components.v1.html(oc_html.replace("{NAME}", "NIFTY 50").replace("{SPOT}", "22,510"), height=350)
    with col_r: st.components.v1.html(oc_html.replace("{NAME}", "BANK NIFTY").replace("{SPOT}", "48,205"), height=350)

# --- 2. STOCK ANALYSIS ---
def page_stock_analysis():
    show_header("PROFESSIONAL STOCK RESEARCH")
    ticker = st.text_input("Enter NSE Ticker", value="RELIANCE").upper()
    if st.button("Generate Pro Report"):
        st.markdown(f"""
        <div style="background:#fff; border:2px solid #b8922e; padding:40px; border-radius:10px; color:#111;">
            <h1 style="font-family:'DM Serif Display'; margin:0;">{ticker} Analysis</h1>
            <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:20px; margin-top:20px;">
                <div class="metric-card">LIVE PRICE<br>₹2,952.40</div>
                <div class="metric-card">MCAP<br>₹18.5L Cr</div>
                <div class="metric-card">P/E<br>25.4</div>
                <div class="metric-card">RISK<br>LOW</div>
            </div>
            <div style="margin-top:30px; background:#111118; color:white; padding:20px; border-radius:10px;">
                <h4 style="color:#b8922e;">HeyFund View</h4>
                <p>Strategic leadership in its sector. Strong accumulation zone near 200-DMA.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- 3. MARKET MOVERS ---
def page_market_movers():
    show_header("MARKET PULSE & VOLUME SHOCKERS")
    c1, c2 = st.columns(2)
    with c1: 
        st.subheader("✅ Top Gainers")
        st.table(pd.DataFrame({'Symbol': ['TATA MOTORS', 'M&M', 'ADANI'], 'LTP': [952, 2450, 3105], 'Change%': ['+4.5%', '+3.2%', '+2.8%']}))
    with c2:
        st.subheader("❌ Top Losers")
        st.table(pd.DataFrame({'Symbol': ['RELIANCE', 'WIPRO', 'HDFCBANK'], 'LTP': [2950, 462, 1512], 'Change%': ['-2.1%', '-1.8%', '-1.5%']}))
    
    st.markdown("---")
    st.subheader("⚡ Top 5 Volume Shockers")
    cols = st.columns(5)
    for i, name in enumerate(["IRFC", "ZOMATO", "RVNL", "BHEL", "IDEA"]):
        with cols[i]:
            st.markdown(f"<div class='metric-card'>{name}<br><span style='font-size:22px; color:#b8922e;'>5.2x</span><br>Vol Spike</div>", unsafe_allow_html=True)

# --- MAIN APP FLOW ---
if st.session_state.angel is None:
    st.markdown("<h1 style='text-align:center; color:#b8922e; font-family:serif;'>HEYFUND LIVE TERMINAL</h1>", unsafe_allow_html=True)
    if st.button("🚀 CONNECT LIVE TO ANGELONE"):
        with st.spinner("Authenticating with SmartAPI..."):
            if connect_angelone():
                st.success("AngelOne Session Generated!")
                st.rerun()
else:
    st.sidebar.image("https://via.placeholder.com/200x60/111118/b8922e?text=HEYFUND", use_container_width=True)
    page = st.sidebar.radio("Navigation", ["Option Chain", "Stock Analysis", "Market Movers"])
    if st.sidebar.button("Logout"):
        st.session_state.angel = None
        st.rerun()

    if page == "Option Chain": page_option_chain()
    elif page == "Stock Analysis": page_stock_analysis()
    elif page == "Market Movers": page_market_movers()
