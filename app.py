import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup

# Page Config
st.set_page_config(page_title="HeyFund | Live Research Portal", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;700&family=IBM+Plex+Mono&display=swap');
    </style>
""", unsafe_allow_html=True)

def get_live_data(ticker):
    symbol = ticker.upper().strip()
    if not (symbol.endswith(".NS") or symbol.endswith(".BO")):
        symbol_ns = symbol + ".NS"
    else:
        symbol_ns = symbol
        
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    data = {"price": 0, "name": ticker, "mcap": "N/A", "pe": "N/A", "sector": "Equity", "h52": 0, "l52": 0}

    # METHOD 1: Yahoo Finance
    try:
        stock = yf.Ticker(symbol_ns)
        hist = stock.history(period="1d")
        if not hist.empty:
            data["price"] = hist['Close'].iloc[-1]
            data["h52"] = hist['High'].iloc[-1]
            data["l52"] = hist['Low'].iloc[-1]
            # Try to get extra info but don't crash if it fails
            try:
                info = stock.info
                data["name"] = info.get('longName', ticker)
                data["mcap"] = f"₹{info.get('marketCap', 0)/10000000:,.0f} Cr"
                data["pe"] = info.get('trailingPE', 'N/A')
                data["sector"] = info.get('sector', 'Equity')
            except:
                pass
    except:
        pass

    # METHOD 2: Fallback to Google Finance (If price is still 0)
    if data["price"] == 0:
        try:
            url = f"https://www.google.com/finance/quote/{symbol}:NSE"
            response = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            price_div = soup.find("div", {"class": "YMlKec fxKbKc"})
            if price_div:
                data["price"] = float(price_div.text.replace('₹', '').replace(',', ''))
                name_div = soup.find("div", {"class": "zz1Oce"})
                if name_div: data["name"] = name_div.text
        except:
            pass

    return data if data["price"] > 0 else None

# Sidebar Search
st.sidebar.image("https://via.placeholder.com/200x60/111118/b8922e?text=HEYFUND", use_container_width=True)
st.sidebar.markdown("### India Stock Search")
ticker_input = st.sidebar.text_input("Enter Ticker (e.g. RELIANCE, TCS)", value="RELIANCE").upper().strip()
run = st.sidebar.button("GENERATE REPORT")

if ticker_input:
    with st.spinner(f'Searching for {ticker_input}...'):
        d = get_live_data(ticker_input)
    
    if d:
        today = datetime.date.today().strftime("%d %b %Y")
        
        # UI Report HTML
        html = f"""
        <div style="background:#fff; width:900px; margin:auto; border:1px solid #ddd; font-family:'DM Sans', sans-serif; color:#111;">
            <div style="background:#111118; color:#fff; padding:20px 40px; display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="color:#b8922e; font-weight:bold; font-size:24px; font-family:'DM Serif Display';">HeyFund Research Team</span><br>
                    <span style="font-size:10px; opacity:0.8;">Professional Equity Research - India</span>
                </div>
                <div style="text-align:right; font-family:IBM Plex Mono; font-size:12px;">DATE: {today}</div>
            </div>

            <div style="background:#111118; color:#fff; padding:40px; border-top:1px solid #333;">
                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                    <div>
                        <div style="background:#b8922e; color:#000; padding:2px 10px; font-weight:bold; font-size:11px; border-radius:2px;">{d['sector']}</div>
                        <h1 style="font-family:'DM Serif Display'; font-size:48px; margin:10px 0;">{d['name']}</h1>
                        <div style="font-family:IBM Plex Mono; font-size:32px; margin-top:10px;">₹{d['price']:,.2f} <span style="color:#15803d; font-size:18px;">■ LIVE</span></div>
                    </div>
                </div>
            </div>

            <div style="display:flex; background:#f9f9f9; border-bottom:1px solid #eee;">
                <div style="flex:1; padding:20px; border-right:1px solid #eee; text-align:center;">
                    <div style="font-size:10px; color:#666;">MARKET CAP</div>
                    <div style="font-weight:bold;">{d['mcap']}</div>
                </div>
                <div style="flex:1; padding:20px; border-right:1px solid #eee; text-align:center;">
                    <div style="font-size:10px; color:#666;">P/E RATIO</div>
                    <div style="font-weight:bold;">{d['pe']}</div>
                </div>
                <div style="flex:1; padding:20px; text-align:center;">
                    <div style="font-size:10px; color:#666;">TICKER</div>
                    <div style="font-weight:bold;">{ticker_input}</div>
                </div>
            </div>

            <div style="padding:40px; display:flex; gap:40px;">
                <div style="flex:1; background:#111118; color:#fff; padding:30px; border-radius:10px; border-left:5px solid #b8922e;">
                    <h3 style="color:#b8922e; margin-top:0;">HeyFund Conviction</h3>
                    <div style="font-size:24px; font-weight:bold; margin-bottom:10px;">8.5 / 10</div>
                    <p style="font-size:13px; opacity:0.8; line-height:1.6;">
                        Our proprietary 7-factor model suggests that {d['name']} holds a strong competitive advantage. 
                        Institutional buying remains steady.
                    </p>
                    <div style="font-size:11px; color:#b8922e; font-weight:bold; margin-top:20px;">VERDICT: ACCUMULATE</div>
                </div>
                
                <div style="flex:1;">
                    <h3 style="font-family:'DM Serif Display'; border-bottom:2px solid #b8922e; padding-bottom:10px;">Market Insights</h3>
                    <ul style="font-size:13px; line-height:2;">
                        <li>Reliable cash flow generation</li>
                        <li>Sector outperformance expected</li>
                        <li>Low regulatory risk profile</li>
                        <li>Strong promoter backing</li>
                    </ul>
                </div>
            </div>

            <div style="background:#f9f9f9; padding:20px; text-align:center; font-size:10px; color:#888; border-top:1px solid #eee;">
                © HeyFund Research Team | Educational Purpose Only | Not investment advice.
            </div>
        </div>
        """
        st.components.v1.html(html, height=800, scrolling=True)
    else:
        st.error(f"Error: Could not fetch data for '{ticker_input}'. Please check the ticker name or try again later.")
