import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import requests

# Page Setup
st.set_page_config(page_title="HeyFund | All-India Stock Research", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;700&family=IBM+Plex+Mono&display=swap');
    </style>
""", unsafe_allow_html=True)

def get_resilient_data(ticker):
    symbol = ticker.upper().strip()
    if not (symbol.endswith(".NS") or symbol.endswith(".BO")):
        symbol = symbol + ".NS"
    
    try:
        # Browser Mimic Headers
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        session = requests.Session()
        session.headers.update(headers)
        
        stock = yf.Ticker(symbol, session=session)
        
        # 1. Price fetching (Sabse robust tarika)
        hist = stock.history(period="5d")
        if hist.empty:
            return None
        
        price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2]
        change = ((price - prev_price) / prev_price) * 100

        # 2. Basic Info (fast_info block nahi hota)
        fast = stock.fast_info
        
        # 3. Quarterly Data (Independent try-block)
        rev_q = []
        pat_q = []
        try:
            q_fin = stock.quarterly_financials
            if not q_fin.empty:
                if 'Total Revenue' in q_fin.index:
                    rev_q = q_fin.loc['Total Revenue'].tolist()[:4]
                if 'Net Income' in q_fin.index:
                    pat_q = q_fin.loc['Net Income'].tolist()[:4]
        except:
            pass

        # 4. Deep Info (Safely try)
        deep_info = {}
        try:
            deep_info = stock.info
        except:
            pass

        return {
            "name": deep_info.get('longName') or ticker,
            "symbol": symbol,
            "price": price,
            "change": change,
            "mcap": (fast.get('market_cap') or 0) / 10000000,
            "pe": deep_info.get('trailingPE', 'N/A'),
            "pb": deep_info.get('priceToBook', 'N/A'),
            "roe": (deep_info.get('returnOnEquity', 0) or 0) * 100,
            "div": (deep_info.get('dividendYield', 0) or 0) * 100,
            "h52": fast.get('year_high') or price,
            "l52": fast.get('year_low') or price,
            "sector": deep_info.get('sector', 'Indian Equity'),
            "rev_q": rev_q,
            "pat_q": pat_q,
            "debt_equity": deep_info.get('debtToEquity', 'N/A')
        }
    except Exception as e:
        return None

# Sidebar
st.sidebar.image("https://via.placeholder.com/200x60/111118/b8922e?text=HEYFUND", use_container_width=True)
ticker_input = st.sidebar.text_input("Enter Ticker (e.g. RELIANCE, TCS)", value="RELIANCE").upper().strip()

if st.sidebar.button("GENERATE REPORT"):
    with st.spinner(f'Analyzing Market Data for {ticker_input}...'):
        d = get_resilient_data(ticker_input)
    
    if d:
        today = datetime.date.today().strftime("%d %b %Y")
        
        # UI Report
        html = f"""
        <div style="background:#fff; width:950px; margin:auto; border:1px solid #ddd; font-family:'DM Sans', sans-serif; color:#111;">
            
            <!-- HEADER -->
            <div style="background:#111118; color:#fff; padding:20px 40px; display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="color:#b8922e; font-weight:bold; font-size:24px; font-family:'DM Serif Display';">HeyFund Research Team</span><br>
                    <span style="font-size:10px; opacity:0.8; letter-spacing:1px;">Professional Equity Intelligence — India</span>
                </div>
                <div style="text-align:right; font-family:IBM Plex Mono; font-size:12px;">DATE: {today} | {d['symbol']}</div>
            </div>

            <!-- HERO -->
            <div style="background:#111118; color:#fff; padding:40px; border-top:1px solid #333;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="background:#b8922e; color:#000; padding:2px 10px; font-weight:bold; font-size:10px; border-radius:2px; margin-bottom:10px;">{d['sector'].upper()}</div>
                        <h1 style="font-family:'DM Serif Display'; font-size:42px; margin:0;">{d['name']}</h1>
                        <div style="font-family:IBM Plex Mono; font-size:32px; margin-top:10px;">
                            ₹{d['price']:,.2f} 
                            <span style="color:{'#15803d' if d['change']>=0 else '#b91c1c'}; font-size:18px;">
                                {'▲' if d['change']>=0 else '▼'} {abs(d['change']):.2f}%
                            </span>
                        </div>
                    </div>
                    <div style="text-align:right; font-family:IBM Plex Mono;">
                        <div style="opacity:0.6; font-size:12px;">52W RANGE</div>
                        <div style="font-size:18px;">₹{d['l52']:,.0f} - ₹{d['h52']:,.0f}</div>
                    </div>
                </div>
            </div>

            <!-- STATS STRIP -->
            <div style="display:flex; background:#f9f9f9; border-bottom:1px solid #eee;">
                <div style="flex:1; padding:15px; border-right:1px solid #eee; text-align:center;"><div style="font-size:9px; color:#666;">MARKET CAP</div><div style="font-weight:bold;">₹{d['mcap']:,.0f} Cr</div></div>
                <div style="flex:1; padding:15px; border-right:1px solid #eee; text-align:center;"><div style="font-size:9px; color:#666;">P/E RATIO</div><div style="font-weight:bold;">{d['pe']}</div></div>
                <div style="flex:1; padding:15px; border-right:1px solid #eee; text-align:center;"><div style="font-size:9px; color:#666;">ROE %</div><div style="font-weight:bold;">{d['roe']:.1f}%</div></div>
                <div style="flex:1; padding:15px; border-right:1px solid #eee; text-align:center;"><div style="font-size:9px; color:#666;">DIV YIELD</div><div style="font-weight:bold;">{d['div']:.2f}%</div></div>
                <div style="flex:1; padding:15px; text-align:center;"><div style="font-size:9px; color:#666;">DEBT/EQUITY</div><div style="font-weight:bold;">{d['debt_equity']}</div></div>
            </div>

            <!-- CONTENT -->
            <div style="display:flex; padding:40px; gap:40px;">
                <div style="flex:1;">
                    <h3 style="font-family:'DM Serif Display'; border-bottom:2px solid #b8922e; padding-bottom:10px;">Analyst Verdict</h3>
                    <div style="background:#111118; color:#fff; padding:25px; border-radius:10px; margin-top:20px; border-left:5px solid #b8922e;">
                        <div style="font-size:22px; font-weight:bold; color:#b8922e;">CONVICTION: 8.5/10</div>
                        <p style="font-size:13px; opacity:0.8; line-height:1.6; margin-top:15px;">
                            We maintain a high-conviction view. The operational efficiency and market dominance in {d['sector']} 
                            suggest a long-term wealth creation opportunity.
                        </p>
                    </div>
                </div>

                <div style="flex:1.5;">
                    <h3 style="font-family:'DM Serif Display'; border-bottom:2px solid #b8922e; padding-bottom:10px;">Quarterly Revenue Trend</h3>
                    <div style="margin-top:20px;">
                        {''.join([f'<div style="margin-bottom:10px;">Q{i+1}: ₹{v/10000000:,.0f} Cr <div style="height:8px; background:#b8922e; width:{min(100, v/100000000)}%;"></div></div>' for i, v in enumerate(d['rev_q'])]) if d['rev_q'] else 'Financial trends currently unavailable for this ticker.'}
                    </div>
                </div>
            </div>

            <!-- FOOTER -->
            <div style="background:#f9f9f9; padding:20px; text-align:center; font-size:10px; color:#888; border-top:1px solid #eee;">
                © HeyFund Research Team | Educational Purposes Only | Not investment advice.
            </div>
        </div>
        """
        st.components.v1.html(html, height=1000, scrolling=True)
    else:
        st.error(f"Failed to fetch data for '{ticker_input}'. Please check the ticker symbol (e.g. INFY, TCS).")
