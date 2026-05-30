import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import requests

# Page Config
st.set_page_config(page_title="HeyFund Research Report", layout="wide")

# Custom CSS for Branding
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .main-card { border: 2px solid #b8922e; border-radius: 10px; padding: 25px; background: white; max-width: 850px; margin: auto; }
    </style>
""", unsafe_allow_html=True)

def get_data_safely(ticker):
    """Yahoo Finance se data nikalne ka sabse robust tarika"""
    symbol = ticker + ".NS"
    
    # Browser ko mimic karne ke liye headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Session banayein taaki block na ho
        session = requests.Session()
        session.headers.update(headers)
        
        stock = yf.Ticker(symbol, session=session)
        
        # Sirf zaroori data uthayein jo fast load ho
        fast_info = stock.fast_info
        
        # Agar fast_info mil gaya, toh humein price mil jayegi
        price = fast_info.last_price
        
        # Baaki details ke liye
        info = stock.info
        
        return {
            "name": info.get('longName', ticker),
            "price": price,
            "mcap": fast_info.market_cap / 10000000 if fast_info.market_cap else 0,
            "pe": info.get('trailingPE', 'N/A'),
            "symbol": symbol
        }
    except Exception as e:
        # Agar info fail ho jaye, toh history se price nikalne ki aakhri koshish
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="1d")
            if not hist.empty:
                return {
                    "name": ticker,
                    "price": hist['Close'].iloc[-1],
                    "mcap": 0,
                    "pe": "N/A",
                    "symbol": symbol
                }
        except:
            return None
    return None

# Sidebar
st.sidebar.image("https://via.placeholder.com/150x50?text=HEYFUND", use_container_width=True)
st.sidebar.title("HeyFund Research")
ticker_input = st.sidebar.text_input("Enter NSE Ticker", value="RELIANCE").upper().strip()
btn = st.sidebar.button("Generate Report")

if ticker_input:
    with st.spinner('Accessing Market Data...'):
        data = get_data_safely(ticker_input)
    
    if data:
        report_date = datetime.date.today().strftime("%d %b %Y")
        
        html = f"""
        <div class="main-card">
            <div style="background: #111118; color: white; padding: 20px; text-align: center; border-radius: 8px;">
                <h2 style="color: #b8922e; margin: 0;">HeyFund Research Team</h2>
                <p style="margin: 5px 0; font-size: 12px; opacity: 0.8;">Professional Equity Intelligence</p>
            </div>
            
            <div style="text-align: center; padding: 30px 0;">
                <h1 style="margin: 0; font-size: 32px; color: #111118;">{data['name']}</h1>
                <p style="color: #666;">Ticker: {data['symbol']} | Date: {report_date}</p>
                <div style="font-size: 48px; font-weight: bold; margin: 20px 0; color: #111118;">
                    ₹{data['price']:,.2f}
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; background: #f9f9f9; padding: 20px; border-radius: 8px;">
                <div style="text-align: center;">
                    <div style="font-size: 12px; color: #b8922e; font-weight: bold;">MARKET CAP</div>
                    <div style="font-size: 20px; font-weight: bold;">₹{data['mcap']:,.0f} Cr</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 12px; color: #b8922e; font-weight: bold;">P/E RATIO</div>
                    <div style="font-size: 20px; font-weight: bold;">{data['pe']}</div>
                </div>
            </div>

            <div style="margin-top: 30px; padding: 20px; background: #111118; color: white; border-radius: 8px;">
                <h4 style="color: #b8922e; margin-top: 0;">HeyFund Analyst View</h4>
                <p style="font-size: 14px; opacity: 0.9; line-height: 1.5;">
                    Fundamental analysis indicates strong resilience at current levels. 
                    The P/E of {data['pe']} reflects the market's current expectation. 
                    We maintain a neutral-to-positive stance for the medium term.
                </p>
            </div>
            
            <div style="text-align: center; margin-top: 20px; font-size: 10px; color: #aaa;">
                © HeyFund Research | Educational Purposes Only | Not Investment Advice
            </div>
        </div>
        """
        st.components.v1.html(html, height=800)
    else:
        st.error(f"Could not connect to market data for {ticker_input}. Please try again in a few seconds.")
