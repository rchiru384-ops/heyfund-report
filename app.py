import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import requests

# --- PAGE CONFIG ---
st.set_page_config(page_title="HeyFund Live Terminal", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;700&family=IBM+Plex+Mono&display=swap');
    </style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- LIVE DATA FETCHING ---
def get_live_stock_data(ticker):
    symbol = ticker.upper().strip()
    if not (symbol.endswith(".NS") or symbol.endswith(".BO")):
        symbol = symbol + ".NS"
    try:
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0'})
        stock = yf.Ticker(symbol, session=session)
        fast = stock.fast_info
        info = stock.info
        
        # Real-time Price
        price = fast.last_price or info.get('currentPrice', 0)
        if price == 0:
            hist = stock.history(period="1d")
            price = hist['Close'].iloc[-1]
            
        return {
            "name": info.get('longName', ticker),
            "symbol": symbol,
            "sector": info.get('sector', 'Equity'),
            "price": price,
            "mcap": fast.market_cap / 10000000,
            "pe": info.get('trailingPE', 'N/A'),
            "roe": (info.get('returnOnEquity', 0) or 0) * 100,
            "h52": fast.year_high,
            "l52": fast.year_low,
            "change": ((price - fast.previous_close) / fast.previous_close) * 100 if fast.previous_close else 0
        }
    except:
        return None

def get_market_movers():
    # NSE Top 10 Tickers scan
    tickers = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "BHARTIARTL.NS", "SBIN.NS", "LICI.NS", "ITC.NS", "HINDUNILVR.NS"]
    data = []
    for t in tickers:
        try:
            s = yf.Ticker(t)
            f = s.fast_info
            chg = ((f.last_price - f.previous_close) / f.previous_close) * 100
            data.append({'Stock': t.replace(".NS",""), 'LTP': f.last_price, 'Change%': chg})
        except: pass
    df = pd.DataFrame(data)
    gainers = df.sort_values(by='Change%', ascending=False).head(5)
    losers = df.sort_values(by='Change%', ascending=True).head(5)
    return gainers, losers

# --- UI PAGES ---
def login_page():
    st.markdown("<h1 style='text-align:center; color:#b8922e;'>HEYFUND PRO LOGIN</h1>", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.text_input("AngelOne Client ID")
            st.text_input("Trading PIN", type="password")
            st.text_input("TOTP Key")
            if st.button("🚀 ENTER LIVE DASHBOARD"):
                st.session_state.logged_in = True
                st.rerun()

def show_analysis():
    st.markdown("<h2 style='color:#b8922e;'>📊 Live Stock Research</h2>", unsafe_allow_html=True)
    t = st.text_input("Enter Ticker", value="RELIANCE").upper()
    if st.button("Generate Live Report"):
        d = get_live_stock_data(t)
        if d:
            color = "#15803d" if d['change'] >= 0 else "#b91c1c"
            html = f"""
            <div style="background:#111118; color:white; padding:40px; border-radius:10px; border-left:8px solid #b8922e; font-family:sans-serif;">
                <h1 style="color:#b8922e; margin:0;">{d['name']}</h1>
                <div style="font-size:32px; margin-top:10px;">₹{d['price']:,.2f} <span style="color:{color}; font-size:18px;">({d['change']:.2f}%)</span></div>
                <hr style="border:0.5px solid #333; margin:20px 0;">
                <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:20px;">
                    <div style="text-align:center;">MCAP<br><b>₹{d['mcap']:,.0f} Cr</b></div>
                    <div style="text-align:center;">P/E<br><b>{d['pe']}</b></div>
                    <div style="text-align:center;">ROE<br><b>{d['roe']:.1f}%</b></div>
                    <div style="text-align:center;">52W HIGH<br><b>₹{d['h52']:,.0f}</b></div>
                </div>
            </div>
            """
            st.components.v1.html(html, height=400)
        else: st.error("Live data not available for this ticker.")

def show_market():
    st.markdown("<h2 style='color:#b8922e;'>🔥 Market Movers (Live)</h2>", unsafe_allow_html=True)
    with st.spinner('Scanning NSE Stocks...'):
        g, l = get_market_movers()
    c1, c2 = st.columns(2)
    with c1: st.success("Top Gainers"); st.table(g)
    with c2: st.error("Top Losers"); st.table(l)

# --- APP FLOW ---
if not st.session_state.logged_in:
    login_page()
else:
    st.sidebar.title("HEYFUND NAVIGATION")
    choice = st.sidebar.radio("Go to:", ["Stock Analysis", "Market Movers", "Option Chain"])
    if choice == "Stock Analysis": show_analysis()
    elif choice == "Market Movers": show_market(); 
    elif choice == "Option Chain": 
        st.title("Live Nifty Spot")
        nifty = yf.Ticker("^NSEI").fast_info.last_price
        st.metric("NIFTY 50", f"₹{nifty:,.2f}")
        st.info("Bhai, jab AngelOne API connect hogi tab yahan pura Split-View Option Chain live ho jayega.")
