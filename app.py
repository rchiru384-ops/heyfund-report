import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# Page Config
st.set_page_config(page_title="HeyFund Research Report", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .report-container { background-color: white; color: #333; font-family: 'DM Sans', sans-serif; }
    </style>
""", unsafe_allow_html=True)

def get_stock_data(ticker):
    try:
        if not ticker.endswith(".NS"):
            ticker = ticker + ".NS"
        stock = yf.Ticker(ticker)
        return stock.info
    except:
        return None

# Sidebar
st.sidebar.title("HeyFund Research")
ticker_input = st.sidebar.text_input("Enter NSE Ticker", value="RELIANCE").upper()
generate_btn = st.sidebar.button("Generate Report")

if ticker_input:
    info = get_stock_data(ticker_input)
    
    if info and 'symbol' in info:
        cmp = info.get('currentPrice', 0)
        long_name = info.get('longName', 'Company')
        risk_score = 45 # Default
        report_date = datetime.date.today().strftime("%d %b %Y")

        # HTML Structure
        html_code = f"""
        <div style="padding: 20px; font-family: sans-serif; border: 2px solid #b8922e; max-width: 800px; margin: auto;">
            <div style="background: #111118; color: white; padding: 20px; text-align: center;">
                <h1 style="color: #b8922e; margin: 0;">HeyFund Research Team</h1>
                <p style="margin: 5px 0;">Independent Equity Research Report</p>
            </div>
            
            <div style="padding: 20px; text-align: center;">
                <h2 style="margin: 0;">{long_name}</h2>
                <p style="font-size: 18px; color: #666;">Ticker: {ticker_input} | Date: {report_date}</p>
                <div style="font-size: 32px; font-weight: bold; color: #111118; margin: 20px 0;">
                    CMP: ₹{cmp:,.2f}
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; padding: 20px; background: #f9f9f9;">
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px;">
                    <h4 style="margin: 0; color: #b8922e;">Market Cap</h4>
                    <p style="font-size: 18px; font-weight: bold;">₹{info.get('marketCap', 0)/10000000:,.0f} Cr</p>
                </div>
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px;">
                    <h4 style="margin: 0; color: #b8922e;">P/E Ratio</h4>
                    <p style="font-size: 18px; font-weight: bold;">{info.get('trailingPE', 'N/A')}</p>
                </div>
            </div>

            <div style="margin-top: 30px; padding: 20px; background: #111118; color: white; border-radius: 8px;">
                <h3 style="color: #b8922e; margin-top: 0;">Analyst Verdict</h3>
                <p>The company shows strong fundamentals with a healthy balance sheet. We recommend a "Watch" on current valuations. Support levels seen at 10% below CMP.</p>
            </div>

            <div style="margin-top: 20px; font-size: 10px; color: #999; text-align: center;">
                Disclaimer: This is for educational purposes only. Not investment advice.
            </div>
        </div>
        """
        st.components.v1.html(html_code, height=800)
    else:
        st.error("Stock not found. Try 'RELIANCE' or 'TATASTEEL'")

else:
    st.info("Please enter a ticker in the sidebar.")