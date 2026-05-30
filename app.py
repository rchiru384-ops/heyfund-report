import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# Page Config
st.set_page_config(page_title="HeyFund Research Report", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

def get_stock_data(ticker):
    # NSE ke liye .NS lagana zaroori hai
    if not (ticker.endswith(".NS") or ticker.endswith(".BO")):
        symbol = ticker + ".NS"
    else:
        symbol = ticker
        
    try:
        stock = yf.Ticker(symbol)
        # Try fetching info
        info = stock.info
        
        # Agar info khali hai, toh price history se nikalne ki koshish karein
        if not info or len(info) < 5:
            hist = stock.history(period="1d")
            if not hist.empty:
                return {
                    'symbol': symbol,
                    'currentPrice': hist['Close'].iloc[-1],
                    'longName': ticker,
                    'marketCap': 0,
                    'trailingPE': 'N/A'
                }
            return None
        return info
    except:
        return None

# Sidebar
st.sidebar.title("HeyFund Research")
ticker_input = st.sidebar.text_input("Enter NSE Ticker (e.g. RELIANCE, TCS)", value="RELIANCE").upper().strip()
generate_btn = st.sidebar.button("Generate Report")

if ticker_input:
    # Spinner dikhayega jab tak data load ho raha hai
    with st.spinner(f'Fetching data for {ticker_input}...'):
        info = get_stock_data(ticker_input)
    
    if info:
        # Data Extraction with safety
        cmp = info.get('currentPrice', info.get('regularMarketPrice', 0))
        name = info.get('longName', info.get('shortName', ticker_input))
        mcap = info.get('marketCap', 0) / 10000000
        pe = info.get('trailingPE', 'N/A')
        
        report_date = datetime.date.today().strftime("%d %b %Y")

        html_code = f"""
        <div style="padding: 20px; font-family: sans-serif; border: 3px solid #b8922e; max-width: 800px; margin: auto; background: white;">
            <div style="background: #111118; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0;">
                <h1 style="color: #b8922e; margin: 0;">HeyFund Research Team</h1>
                <p style="margin: 5px 0; opacity: 0.8;">Independent Equity Research Report</p>
            </div>
            
            <div style="padding: 30px; text-align: center;">
                <h2 style="margin: 0; color: #111118; font-size: 28px;">{name}</h2>
                <p style="font-size: 16px; color: #666;">Ticker: {info.get('symbol')} | Date: {report_date}</p>
                <div style="font-size: 42px; font-weight: bold; color: #111118; margin: 20px 0;">
                    ₹{cmp:,.2f}
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; padding: 20px; background: #fdf9f0; border-radius: 10px;">
                <div style="text-align: center; border-right: 1px solid #ddd;">
                    <h4 style="margin: 0; color: #b8922e; text-transform: uppercase; font-size: 12px;">Market Cap</h4>
                    <p style="font-size: 20px; font-weight: bold; margin: 5px 0;">₹{mcap:,.0f} Cr</p>
                </div>
                <div style="text-align: center;">
                    <h4 style="margin: 0; color: #b8922e; text-transform: uppercase; font-size: 12px;">P/E Ratio</h4>
                    <p style="font-size: 20px; font-weight: bold; margin: 5px 0;">{pe}</p>
                </div>
            </div>

            <div style="margin-top: 30px; padding: 20px; background: #111118; color: white; border-radius: 10px;">
                <h3 style="color: #b8922e; margin-top: 0; border-bottom: 1px solid #333; padding-bottom: 10px;">HeyFund View</h3>
                <p style="line-height: 1.6; opacity: 0.9;">
                    The stock is currently showing stable momentum. Based on the {pe} P/E ratio and sector trends, 
                    investors should look for entry points near support levels. Fundamentals remain intact.
                </p>
            </div>

            <div style="margin-top: 20px; font-size: 11px; color: #999; text-align: center;">
                <b>Disclaimer:</b> Research by HeyFund Research Team. For educational purposes only. Not SEBI registered.
            </div>
        </div>
        """
        st.components.v1.html(html_code, height=850, scrolling=True)
    else:
        st.error(f"Could not find data for '{ticker_input}'. Please make sure it's a valid NSE ticker.")

else:
    st.info("Enter a ticker like RELIANCE, TCS, or TATASTEEL to begin.")
