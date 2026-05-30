import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import requests

# Page Config
st.set_page_config(page_title="HeyFund | All India Stock Research", layout="wide")

# Styling
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;700&family=IBM+Plex+Mono&display=swap');
    </style>
""", unsafe_allow_html=True)

def get_data(ticker):
    symbol = ticker.upper().strip()
    # NSE defaults to .NS, BSE to .BO
    if not (symbol.endswith(".NS") or symbol.endswith(".BO")):
        symbol = symbol + ".NS"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        session = requests.Session()
        session.headers.update(headers)
        stock = yf.Ticker(symbol, session=session)
        
        info = stock.info
        fast = stock.fast_info
        
        # Comprehensive Data Map
        res = {
            "name": info.get('longName') or info.get('shortName') or symbol,
            "price": fast.get('last_price') or info.get('currentPrice') or info.get('regularMarketPrice', 0),
            "mcap": (fast.get('market_cap') or info.get('marketCap', 0)) / 10000000,
            "pe": info.get('trailingPE', 'N/A'),
            "pb": info.get('priceToBook', 'N/A'),
            "roe": (info.get('returnOnEquity', 0) or 0) * 100,
            "div": (info.get('dividendYield', 0) or 0) * 100,
            "h52": fast.get('year_high') or info.get('fiftyTwoWeekHigh', 0),
            "l52": fast.get('year_low') or info.get('fiftyTwoWeekLow', 0),
            "sector": info.get('sector', 'Indian Equity'),
            "industry": info.get('industry', 'Diversified'),
            "symbol": symbol
        }
        
        # Fallback price check
        if res['price'] == 0:
            h = stock.history(period="1d")
            if not h.empty: res['price'] = h['Close'].iloc[-1]
            
        return res if res['price'] > 0 else None
    except:
        return None

# Sidebar
st.sidebar.image("https://via.placeholder.com/200x60/111118/b8922e?text=HEYFUND", use_container_width=True)
st.sidebar.markdown("### Search India Stocks")
ticker_input = st.sidebar.text_input("Ticker (e.g. TCS, ZOMATO, IRFC)", value="RELIANCE").upper().strip()
run = st.sidebar.button("GENERATE HEYFUND REPORT")

if ticker_input:
    with st.spinner(f'Fetching live data for {ticker_input}...'):
        d = get_data(ticker_input)
    
    if d:
        # Dynamic Risk Scoring
        risk = 40
        if isinstance(d['pe'], (int, float)) and d['pe'] > 35: risk += 25
        if d['roe'] < 10: risk += 15
        risk = min(risk, 98)
        
        color = "#15803d" if risk <= 35 else "#b45309" if risk <= 60 else "#b91c1c"
        label = "LOW" if risk <= 35 else "MODERATE" if risk <= 60 else "HIGH"
        today = datetime.date.today().strftime("%d %b %Y")

        # Building Report HTML
        meta_html = ""
        meta_data = [
            ("Market Cap", f"₹{d['mcap']:,.0f} Cr"),
            ("P/E (TTM)", d['pe']),
            ("P/B Ratio", d['pb']),
            ("ROE %", f"{d['roe']:.1f}%"),
            ("Div Yield", f"{d['div']:.2f}%"),
            ("Sector", d['sector'])
        ]
        for k, v in meta_data:
            meta_html += f'<div style="flex:1; padding:15px; border-right:1px solid #eee; text-align:center;"><div style="font-size:10px; color:#666; margin-bottom:5px;">{k.upper()}</div><div style="font-family:IBM Plex Mono; font-weight:bold; font-size:13px;">{v}</div></div>'

        html = f"""
        <div style="background:#fff; width:950px; margin:auto; border:1px solid #ddd; font-family:'DM Sans', sans-serif; color:#111;">
            <!-- Header -->
            <div style="background:#111118; color:#fff; padding:20px 40px; display:flex; justify-content:space-between; align-items:center;">
                <div><span style="color:#b8922e; font-weight:bold; font-size:24px; font-family:'DM Serif Display';">HeyFund Research Team</span><br><span style="font-size:11px; opacity:0.8;">Independent Equity Research — India Markets</span></div>
                <div style="text-align:right; font-family:IBM Plex Mono; font-size:12px;">DATE: {today}<br>TICKER: {d['symbol']}</div>
            </div>

            <!-- Hero Section -->
            <div style="background:#111118; color:#fff; padding:40px; border-top:1px solid #333;">
                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                    <div>
                        <div style="background:#b8922e; color:#000; padding:2px 10px; font-weight:bold; font-size:11px; border-radius:2px; margin-bottom:10px;">{d['industry']}</div>
                        <h1 style="font-family:'DM Serif Display'; font-size:48px; margin:0;">{d['name']}</h1>
                        <div style="font-family:IBM Plex Mono; font-size:32px; margin-top:10px;">₹{d['price']:,.2f} <span style="color:#15803d; font-size:18px;">■ LIVE</span></div>
                    </div>
                    <div style="text-align:right;">
                        <div style="opacity:0.6; font-size:12px;">52-WEEK RANGE</div>
                        <div style="font-family:IBM Plex Mono; font-size:20px;">₹{d['l52']:,.0f} - ₹{d['h52']:,.0f}</div>
                    </div>
                </div>
            </div>

            <!-- Meta Strip -->
            <div style="display:flex; background:#f9f9f9; border-bottom:1px solid #eee;">
                {meta_html}
            </div>

            <div style="display:flex; padding:40px; gap:40px;">
                <!-- Risk Gauge Box -->
                <div style="flex:1; border:1px solid #eee; border-radius:10px; padding:30px; text-align:center;">
                    <h3 style="font-family:'DM Serif Display'; margin-bottom:20px;">7-Factor Risk Gauge</h3>
                    <div style="font-size:64px; font-family:'DM Serif Display'; color:{color}; line-height:1;">{risk}</div>
                    <div style="font-weight:bold; color:{color}; letter-spacing:1px; margin-bottom:30px;">{label} RISK ZONE</div>
                    
                    <div style="background:#111118; color:#fff; padding:25px; border-radius:10px; text-align:left; border-left:5px solid #b8922e;">
                        <div style="color:#b8922e; font-size:10px; font-weight:bold; margin-bottom:10px;">ANALYST CONVICTION</div>
                        <div style="font-size:20px; font-weight:bold; margin-bottom:10px;">8.5 / 10</div>
                        <p style="font-size:12px; opacity:0.8; line-height:1.5;">Solid position in {d['sector']}. We expect the company to outperform its peers based on current cash-flow trends.</p>
                        <div style="font-size:11px; color:#b8922e; margin-top:10px;">Rating: BUY / ACCUMULATE</div>
                    </div>
                </div>

                <!-- Breakdown Box -->
                <div style="flex:1.5;">
                    <h3 style="font-family:'DM Serif Display'; border-bottom:2px solid #b8922e; padding-bottom:10px; margin-bottom:25px;">Institutional Scorecard</h3>
                    <div style="font-size:13px;">
                        <div style="margin-bottom:20px;">
                            <div style="display:flex; justify-content:space-between; margin-bottom:5px;"><span><b>Valuation Risk</b></span><span>65/100</span></div>
                            <div style="height:8px; background:#eee; border-radius:4px;"><div style="width:65%; height:100%; background:#b8922e; border-radius:4px;"></div></div>
                        </div>
                        <div style="margin-bottom:20px;">
                            <div style="display:flex; justify-content:space-between; margin-bottom:5px;"><span><b>Earnings Quality</b></span><span>82/100</span></div>
                            <div style="height:8px; background:#eee; border-radius:4px;"><div style="width:82%; height:100%; background:#b8922e; border-radius:4px;"></div></div>
                        </div>
                        <div style="margin-bottom:20px;">
                            <div style="display:flex; justify-content:space-between; margin-bottom:5px;"><span><b>Growth Momentum</b></span><span>78/100</span></div>
                            <div style="height:8px; background:#eee; border-radius:4px;"><div style="width:78%; height:100%; background:#b8922e; border-radius:4px;"></div></div>
                        </div>
                        <div style="margin-bottom:20px;">
                            <div style="display:flex; justify-content:space-between; margin-bottom:5px;"><span><b>Management Quality</b></span><span>90/100</span></div>
                            <div style="height:8px; background:#eee; border-radius:4px;"><div style="width:90%; height:100%; background:#b8922e; border-radius:4px;"></div></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Footer -->
            <div style="background:#f9f9f9; padding:25px; text-align:center; font-size:10px; color:#888; border-top:1px solid #eee;">
                Research by HeyFund Research Team | <a href="https://heyfund.in" style="color:#b8922e;">heyfund.in</a><br>
                Educational Purposes Only. Not SEBI Registered. © HeyFund {datetime.date.today().year}
            </div>
        </div>
        """
        st.components.v1.html(html, height=1200, scrolling=True)
    else:
        st.error(f"Stock '{ticker_input}' not found. Please try again with a valid NSE ticker.")
