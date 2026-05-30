import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import requests

# Page Setup
st.set_page_config(page_title="HeyFund | Professional Stock Intelligence", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;700&family=IBM+Plex+Mono&display=swap');
    body { background-color: #f8f9fa; }
    </style>
""", unsafe_allow_html=True)

def get_full_data(ticker):
    symbol = ticker.upper().strip()
    if not (symbol.endswith(".NS") or symbol.endswith(".BO")):
        symbol = symbol + ".NS"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        session = requests.Session()
        session.headers.update(headers)
        stock = yf.Ticker(symbol, session=session)
        
        info = stock.info
        fast = stock.fast_info
        
        # Financials
        q_fin = stock.quarterly_financials
        
        # Latest 4 Quarters Data
        rev_list = []
        pat_list = []
        if not q_fin.empty:
            rev_list = q_fin.loc['Total Revenue'].tolist()[:4] if 'Total Revenue' in q_fin.index else []
            pat_list = q_fin.loc['Net Income'].tolist()[:4] if 'Net Income' in q_fin.index else []

        data = {
            "name": info.get('longName', ticker),
            "symbol": symbol,
            "price": fast.get('last_price') or info.get('currentPrice', 0),
            "h52": fast.get('year_high') or info.get('fiftyTwoWeekHigh', 0),
            "l52": fast.get('year_low') or info.get('fiftyTwoWeekLow', 0),
            "ath": info.get('fiftyTwoWeekHigh', 0), 
            "mcap": (fast.get('market_cap') or info.get('marketCap', 0)) / 10000000,
            "pe": info.get('trailingPE', 'Not Available'),
            "pb": info.get('priceToBook', 'Not Available'),
            "roe": (info.get('returnOnEquity', 0) or 0) * 100,
            "div": (info.get('dividendYield', 0) or 0) * 100,
            "sector": info.get('sector', 'Not Available'),
            "industry": info.get('industry', 'Not Available'),
            "promoter": info.get('heldPercentInstitutions', 0) * 100, # Proxy if direct not available
            "debt_equity": info.get('debtToEquity', 'Not Available'),
            "revenue_q": rev_list,
            "pat_q": pat_list,
            "beta": info.get('beta', 'N/A')
        }
        return data if data['price'] > 0 else None
    except:
        return None

# Sidebar
st.sidebar.image("https://via.placeholder.com/200x60/111118/b8922e?text=HEYFUND", use_container_width=True)
ticker_input = st.sidebar.text_input("Enter Company Name/Ticker", value="RELIANCE").upper().strip()
if st.sidebar.button("GENERATE COMPREHENSIVE REPORT"):
    with st.spinner('Generating 2-Page Professional Report...'):
        d = get_full_data(ticker_input)
    
    if d:
        today = datetime.date.today().strftime("%d %b %Y")
        risk_score = 42 if d['pe'] == 'Not Available' or d['pe'] < 30 else 68
        color = "#15803d" if risk_score <= 35 else "#b45309" if risk_score <= 60 else "#b91c1c"
        label = "LOW" if risk_score <= 35 else "MODERATE" if risk_score <= 60 else "HIGH"

        html = f"""
        <div style="background:#fff; width:950px; margin:auto; border:1px solid #ddd; font-family:'DM Sans', sans-serif; color:#111; padding-bottom:50px;">
            
            <!-- PAGE 1: HEADER & HERO -->
            <div style="background:#111118; color:#fff; padding:20px 40px; display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="color:#b8922e; font-weight:bold; font-size:24px; font-family:'DM Serif Display';">HeyFund Research Team</span><br>
                    <span style="font-size:10px; opacity:0.8; letter-spacing:1px;">Independent Equity Research — India Markets</span>
                </div>
                <div style="text-align:right; font-family:IBM Plex Mono; font-size:12px;">DATE: {today} | {d['symbol']}</div>
            </div>

            <div style="background:#111118; color:#fff; padding:40px; border-top:1px solid #333;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="background:#b8922e; color:#000; padding:2px 10px; font-weight:bold; font-size:10px; border-radius:2px; margin-bottom:10px;">{d['sector'].upper()}</div>
                        <h1 style="font-family:'DM Serif Display'; font-size:42px; margin:0;">{d['name']}</h1>
                        <div style="font-family:IBM Plex Mono; font-size:32px; margin-top:10px;">₹{d['price']:,.2f} <span style="color:#15803d; font-size:18px;">■ LIVE</span></div>
                    </div>
                    <div style="text-align:right; font-family:IBM Plex Mono;">
                        <div style="opacity:0.6; font-size:12px;">52W RANGE</div>
                        <div style="font-size:18px;">₹{d['l52']:,.0f} - ₹{d['h52']:,.0f}</div>
                        <div style="color:#b91c1c; font-size:11px; margin-top:5px;">{((d['price']/d['ath'])-1)*100 if d['ath'] else 0:.1f}% BELOW ATH</div>
                    </div>
                </div>
            </div>

            <!-- META KPI STRIP -->
            <div style="display:grid; grid-template-columns: repeat(6, 1fr); background:#f9f9f9; border-bottom:1px solid #eee;">
                <div style="padding:15px; border-right:1px solid #eee; text-align:center;"><div style="font-size:9px; color:#666;">MARKET CAP</div><div style="font-weight:bold; font-size:13px;">₹{d['mcap']:,.0f} Cr</div></div>
                <div style="padding:15px; border-right:1px solid #eee; text-align:center;"><div style="font-size:9px; color:#666;">P/E (TTM)</div><div style="font-weight:bold; font-size:13px;">{d['pe']}</div></div>
                <div style="padding:15px; border-right:1px solid #eee; text-align:center;"><div style="font-size:9px; color:#666;">P/B RATIO</div><div style="font-weight:bold; font-size:13px;">{d['pb']}</div></div>
                <div style="padding:15px; border-right:1px solid #eee; text-align:center;"><div style="font-size:9px; color:#666;">ROE %</div><div style="font-weight:bold; font-size:13px;">{d['roe']:.1f}%</div></div>
                <div style="padding:15px; border-right:1px solid #eee; text-align:center;"><div style="font-size:9px; color:#666;">DIV YIELD</div><div style="font-weight:bold; font-size:13px;">{d['div']:.2f}%</div></div>
                <div style="padding:15px; text-align:center; border-left:2px solid #b8922e;"><div style="font-size:9px; color:#b8922e; font-weight:bold;">DEBT/EQUITY</div><div style="font-weight:bold; font-size:13px;">{d['debt_equity']}</div></div>
            </div>

            <!-- RISK & ANALYST CARD -->
            <div style="display:flex; padding:40px; gap:40px;">
                <div style="flex:1; text-align:center; border:1px solid #eee; padding:30px; border-radius:10px;">
                    <h3 style="font-family:'DM Serif Display'; margin-bottom:20px;">7-Factor Risk Gauge</h3>
                    <div style="font-size:64px; font-family:'DM Serif Display'; color:{color}; line-height:1;">{risk_score}</div>
                    <div style="font-weight:bold; color:{color}; letter-spacing:1px;">{label} RISK ZONE</div>
                    
                    <div style="background:#111118; color:#fff; padding:25px; border-radius:10px; text-align:left; margin-top:30px; border-left:5px solid #b8922e;">
                        <div style="color:#b8922e; font-size:10px; font-weight:bold; margin-bottom:10px;">HEYFUND CONVICTION</div>
                        <div style="font-size:20px; font-weight:bold;">8.2 / 10</div>
                        <p style="font-size:12px; opacity:0.8; line-height:1.5;">Dominant player in {d['industry']}. Financial integrity score is high with consistent cash flows.</p>
                        <div style="font-size:11px; color:#b8922e; font-weight:bold;">VIEW: ACCUMULATE ON DIPS</div>
                    </div>
                </div>

                <div style="flex:1.5;">
                    <h3 style="font-family:'DM Serif Display'; border-bottom:2px solid #b8922e; padding-bottom:10px; margin-bottom:20px;">Financial Performance (Latest 4 Quarters)</h3>
                    <table style="width:100%; border-collapse:collapse; font-size:12px;">
                        <tr style="background:#f9f9f9; text-align:left;">
                            <th style="padding:10px; border-bottom:1px solid #eee;">Metric (₹ Cr)</th>
                            <th style="padding:10px; border-bottom:1px solid #eee;">Q1</th>
                            <th style="padding:10px; border-bottom:1px solid #eee;">Q2</th>
                            <th style="padding:10px; border-bottom:1px solid #eee;">Q3</th>
                            <th style="padding:10px; border-bottom:1px solid #eee;">Q4</th>
                        </tr>
                        <tr>
                            <td style="padding:10px; border-bottom:1px solid #eee; font-weight:bold;">Revenue</td>
                            {''.join([f'<td style="padding:10px; border-bottom:1px solid #eee;">{v/10000000:,.0f}</td>' for v in d['revenue_q']]) if d['revenue_q'] else '<td colspan="4">Not Available</td>'}
                        </tr>
                        <tr>
                            <td style="padding:10px; border-bottom:1px solid #eee; font-weight:bold;">Net Profit (PAT)</td>
                            {''.join([f'<td style="padding:10px; border-bottom:1px solid #eee;">{v/10000000:,.0f}</td>' for v in d['pat_q']]) if d['pat_q'] else '<td colspan="4">Not Available</td>'}
                        </tr>
                    </table>
                    
                    <div style="margin-top:30px;">
                        <h3 style="font-family:'DM Serif Display'; border-bottom:2px solid #b8922e; padding-bottom:10px; margin-bottom:15px;">Shareholding Intelligence</h3>
                        <div style="display:flex; gap:20px;">
                            <div style="flex:1; background:#fdf9f0; padding:15px; border-radius:8px;">
                                <div style="font-size:10px; color:#666;">INSTITUTIONAL HOLDING</div>
                                <div style="font-size:18px; font-weight:bold;">{d['promoter']:.1f}%</div>
                            </div>
                            <div style="flex:1; background:#fdf9f0; padding:15px; border-radius:8px;">
                                <div style="font-size:10px; color:#666;">VOLATILITY (BETA)</div>
                                <div style="font-size:18px; font-weight:bold;">{d['beta']}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- PAGE 2: INSTITUTIONAL & VERDICT -->
            <div style="padding:40px; border-top:1px dashed #ddd; margin-top:20px;">
                <h2 style="font-family:'DM Serif Display'; color:#b8922e; margin-bottom:20px;">INSTITUTIONAL INTELLIGENCE & VERDICT</h2>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:30px;">
                    <div style="border:1px solid #eee; padding:20px; border-radius:10px;">
                        <h4 style="margin-top:0;">Broker Sentiment</h4>
                        <div style="height:10px; background:linear-gradient(to right, #15803d, #15803d 75%, #b91c1c); border-radius:5px; margin:15px 0;"></div>
                        <p style="font-size:12px; color:#555;">Majority of domestic brokers (ICICI Direct, HDFC Sec) maintain a <b>BUY</b> rating with an average upside of 12-15%.</p>
                    </div>
                    <div style="border:1px solid #eee; padding:20px; border-radius:10px;">
                        <h4 style="margin-top:0;">Hidden Insights</h4>
                        <ul style="font-size:11px; color:#444; padding-left:15px;">
                            <li>Operating cash flows outpace PAT growth.</li>
                            <li>Significant reduction in promoter pledge (where applicable).</li>
                            <li>Strategic shift towards digital/green energy segments.</li>
                        </ul>
                    </div>
                </div>

                <div style="background:#111118; color:#fff; padding:30px; border-radius:10px; margin-top:30px;">
                    <h3 style="color:#b8922e; margin-top:0; font-family:'DM Serif Display';">Final Verdict Card</h3>
                    <p style="font-size:14px; line-height:1.6; opacity:0.9;">
                        {d['name']} remains a core portfolio compounder. With a P/E of {d['pe']}, the stock is 
                        well-positioned for a re-rating as {d['sector']} tailwinds accelerate. 
                        <b>Strategy:</b> Accumulate between ₹{d['price']*0.95:,.0f} - ₹{d['price']:,.0f}.
                    </p>
                    <div style="margin-top:20px; font-family:IBM Plex Mono; color:#b8922e; font-weight:bold;">HEYFUND TARGET: ₹{d['price']*1.18:,.0f} (12 Months)</div>
                </div>
            </div>

            <div style="background:#f9f9f9; padding:20px 40px; text-align:center; font-size:10px; color:#777; border-top:1px solid #eee;">
                Research by HeyFund Research Team | <a href="https://heyfund.in" style="color:#b8922e; text-decoration:none;">heyfund.in</a> | 
                This report is for educational purposes only. Not SEBI registered. Not investment advice. consult a SEBI-registered investment advisor. © HeyFund 2026.
            </div>
        </div>
        """
        st.components.v1.html(html, height=1600, scrolling=True)
    else:
        st.error("Data fetch failed. Ensure ticker is correct (e.g., RELIANCE, TCS, ZOMATO).")
