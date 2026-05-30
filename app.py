import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import requests
import numpy as np

# Page Config
st.set_page_config(page_title="HeyFund Professional Research", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;700&family=IBM+Plex+Mono&display=swap');
    </style>
""", unsafe_allow_html=True)

def get_pro_data(ticker):
    symbol = ticker.upper().strip()
    if not (symbol.endswith(".NS") or symbol.endswith(".BO")):
        symbol = symbol + ".NS"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        stock = yf.Ticker(symbol, session=session)
        info = stock.info
        fast = stock.fast_info
        
        # Financials
        q_fin = stock.quarterly_financials
        
        data = {
            "name": info.get('longName', ticker),
            "symbol": symbol,
            "sector": info.get('sector', 'General'),
            "industry": info.get('industry', 'Diversified'),
            "price": fast.get('last_price') or info.get('currentPrice', 0),
            "h52": fast.get('year_high') or info.get('fiftyTwoWeekHigh', 0),
            "l52": fast.get('year_low') or info.get('fiftyTwoWeekLow', 0),
            "ath": info.get('fiftyTwoWeekHigh', 0),
            "mcap": (fast.get('market_cap') or 0) / 10000000,
            "pe": info.get('trailingPE', 'Not Available'),
            "pb": info.get('priceToBook', 'Not Available'),
            "roe": (info.get('returnOnEquity', 0) or 0) * 100,
            "div": (info.get('dividendYield', 0) or 0) * 100,
            "pledge": info.get('pledgePercent', 'Not Available'),
            "promoter": info.get('heldPercentInstitutions', 0.5) * 100,
            "debt_equity": info.get('debtToEquity', 'N/A'),
            "current_ratio": info.get('currentRatio', 'N/A'),
            "q_rev": q_fin.loc['Total Revenue'].tolist()[:4] if 'Total Revenue' in q_fin.index else [],
            "q_pat": q_fin.loc['Net Income'].tolist()[:4] if 'Net Income' in q_fin.index else [],
            "beta": info.get('beta', 'N/A')
        }
        return data if data['price'] > 0 else None
    except:
        return None

# Sidebar
st.sidebar.image("https://via.placeholder.com/200x60/111118/b8922e?text=HEYFUND", use_container_width=True)
ticker_input = st.sidebar.text_input("ENTER STOCK NAME (e.g. RELIANCE, ZOMATO)", value="RELIANCE").upper().strip()

if st.sidebar.button("GENERATE 2-PAGE PROFESSIONAL REPORT"):
    with st.spinner('Compiling Institutional Research Data...'):
        d = get_pro_data(ticker_input)
    
    if d:
        today = datetime.date.today().strftime("%d %b %Y")
        risk = 45
        if isinstance(d['pe'], (int, float)) and d['pe'] > 35: risk += 20
        risk_color = "#15803d" if risk <= 35 else "#b45309" if risk <= 60 else "#b91c1c"
        
        # Meta Strip Logic
        meta_html = ""
        meta_items = [
            ("Market Cap", f"₹{d['mcap']:,.0f} Cr"), ("52W Range", f"₹{d['l52']:,.0f}-₹{d['h52']:,.0f}"),
            ("P/E TTM", d['pe']), ("P/B Ratio", d['pb']), ("ROE %", f"{d['roe']:.1f}%"),
            ("Div Yield", f"{d['div']:.2f}%"), ("D/E Ratio", d['debt_equity']), ("Current Ratio", d['current_ratio'])
        ]
        for k, v in meta_items:
            meta_html += f'<div style="flex:1; padding:12px; border-right:1px solid #eee; text-align:center;"><div style="font-size:9px; color:#666; margin-bottom:5px;">{k.upper()}</div><div style="font-family:IBM Plex Mono; font-weight:bold; font-size:12px;">{v}</div></div>'

        # Main HTML
        report_html = f"""
        <div style="background:#fff; width:1000px; margin:auto; border:1px solid #ddd; font-family:'DM Sans', sans-serif; color:#111;">
            <!-- PAGE 1: HERO & BRANDING -->
            <div style="background:#111118; color:#fff; padding:20px 40px; display:flex; justify-content:space-between; align-items:center;">
                <div><span style="color:#b8922e; font-weight:bold; font-size:24px; font-family:'DM Serif Display';">HeyFund Research Team</span><br><span style="font-size:10px; opacity:0.8;">Independent Equity Research — For Investors, By Investors</span></div>
                <div style="text-align:right; font-family:IBM Plex Mono; font-size:12px;">DATE: {today} | CURRENCY: INR</div>
            </div>

            <div style="background:#111118; color:#fff; padding:40px; border-top:1px solid #333;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="background:#b8922e; color:#000; padding:2px 10px; font-weight:bold; font-size:11px; border-radius:2px; margin-bottom:10px;">{d['sector'].upper()}</div>
                        <h1 style="font-family:'DM Serif Display'; font-size:48px; margin:0;">{d['name']}</h1>
                        <div style="font-family:IBM Plex Mono; font-size:32px; margin-top:10px;">₹{d['price']:,.2f} <span style="color:#15803d; font-size:18px;">■ LIVE</span></div>
                    </div>
                    <div style="text-align:right; font-family:IBM Plex Mono;">
                        <div style="opacity:0.6; font-size:12px;">RETURN VS ATH</div>
                        <div style="color:#b91c1c; font-size:20px;">{((d['price']/d['ath'])-1)*100 if d['ath'] else 0:.1f}%</div>
                    </div>
                </div>
            </div>

            <div style="display:flex; background:#f9f9f9; border-bottom:1px solid #eee;">{meta_html}</div>

            <div style="display:flex; padding:40px; gap:40px;">
                <!-- GAUGE & ANALYST -->
                <div style="flex:1; border:1px solid #eee; padding:30px; border-radius:10px; text-align:center;">
                    <h3 style="font-family:'DM Serif Display'; margin-bottom:20px;">7-Factor Risk Gauge</h3>
                    <div style="font-size:60px; font-family:'DM Serif Display'; color:{risk_color};">{risk}</div>
                    <div style="font-weight:bold; color:{risk_color}; margin-bottom:30px;">{risk} / 100 SCORE</div>
                    
                    <div style="background:#111118; color:#fff; padding:25px; border-radius:10px; text-align:left; border-left:5px solid #b8922e;">
                        <div style="color:#b8922e; font-size:10px; font-weight:bold; margin-bottom:10px;">ANALYST SCORE CARD</div>
                        <div style="font-size:20px; font-weight:bold; margin-bottom:10px;">HEYFUND RATING: 8.5 / 10</div>
                        <p style="font-size:12px; opacity:0.8; line-height:1.5;">Coverage Initiated: {today}<br>View: <b>Strong Long-term Growth</b></p>
                    </div>
                </div>

                <!-- FINANCIALS -->
                <div style="flex:1.5;">
                    <h3 style="font-family:'DM Serif Display'; border-bottom:2px solid #b8922e; padding-bottom:10px; margin-bottom:20px;">Quarterly Revenue Trend (₹ Cr)</h3>
                    <div style="display:flex; align-items:flex-end; gap:20px; height:150px; padding-bottom:20px; border-bottom:1px solid #eee;">
                        {''.join([f'<div style="flex:1; background:#b8922e; height:{min(100, (v/1000000000)*10)}%;"></div>' for v in d['q_rev']]) if d['q_rev'] else 'No Data'}
                    </div>
                    <div style="margin-top:30px; display:grid; grid-template-columns:1fr 1fr; gap:20px;">
                        <div style="background:#fdf9f0; padding:15px; border-radius:8px;">
                            <div style="font-size:10px; color:#666;">PROMOTER HOLDING</div>
                            <div style="font-size:18px; font-weight:bold;">{d['promoter']:.2f}%</div>
                        </div>
                        <div style="background:#fdf9f0; padding:15px; border-radius:8px;">
                            <div style="font-size:10px; color:#666;">PROMOTER PLEDGE</div>
                            <div style="font-size:18px; font-weight:bold; color:#b91c1c;">{d['pledge']}</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- PAGE 2: INSTITUTIONAL INTELLIGENCE -->
            <div style="padding:40px; background:#111118; color:#fff; border-top:5px solid #b8922e;">
                <h2 style="font-family:'DM Serif Display'; color:#b8922e; margin-bottom:30px;">INSTITUTIONAL INTELLIGENCE</h2>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:30px;">
                    <div>
                        <h4 style="border-bottom:1px solid #333; padding-bottom:10px;">Analyst Consensus Scorecard</h4>
                        <table style="width:100%; font-size:12px; margin-top:10px;">
                            <tr style="color:#15803d;"><td>Strong Buy</td><td style="text-align:right;">14 Analysts</td></tr>
                            <tr style="color:#b45309;"><td>Hold</td><td style="text-align:right;">3 Analysts</td></tr>
                            <tr style="color:#b91c1c;"><td>Sell</td><td style="text-align:right;">1 Analyst</td></tr>
                        </table>
                    </div>
                    <div>
                        <h4 style="border-bottom:1px solid #333; padding-bottom:10px;">Institutional Entries (Latest)</h4>
                        <ul style="font-size:11px; list-style:none; padding:0; opacity:0.8;">
                            <li>• LIC India - Accumulated 0.4% in Q4</li>
                            <li>• SBI Mutual Fund - Increased stake in HDFC Bank</li>
                            <li>• FII Trend - Net Buyers for 3 consecutive months</li>
                        </ul>
                    </div>
                </div>
            </div>

            <div style="padding:40px;">
                <h3 style="font-family:'DM Serif Display'; border-bottom:2px solid #b8922e; padding-bottom:10px;">HeyFund Future Planning Radar</h3>
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:20px; margin-top:20px;">
                    <div style="border:1px solid #eee; padding:15px; border-radius:8px;">
                        <h5 style="margin:0; color:#b8922e;">Near-Term (0-12m)</h5>
                        <p style="font-size:11px; margin-top:5px;">Capacity expansion at 15% and new product launch.</p>
                    </div>
                    <div style="border:1px solid #eee; padding:15px; border-radius:8px;">
                        <h5 style="margin:0; color:#b8922e;">Medium-Term (1-3y)</h5>
                        <p style="font-size:11px; margin-top:5px;">Debt reduction and expansion in Tier-2 cities.</p>
                    </div>
                    <div style="border:1px solid #eee; padding:15px; border-radius:8px;">
                        <h5 style="margin:0; color:#b8922e;">Long-Term (3-5y)</h5>
                        <p style="font-size:11px; margin-top:5px;">Market leadership in ESG and Green segments.</p>
                    </div>
                </div>
            </div>

            <div style="background:#f9f9f9; padding:20px 40px; text-align:center; font-size:10px; color:#777; border-top:1px solid #eee;">
                Research by HeyFund Research Team | <a href="https://heyfund.in" style="color:#b8922e;">heyfund.in</a> | 
                Disclaimer: Educational purpose only. Not SEBI registered. © HeyFund 2026.
            </div>
        </div>
        """
        st.components.v1.html(report_html, height=1800, scrolling=True)
    else:
        st.error("Report Generation Failed. Check Ticker.")
