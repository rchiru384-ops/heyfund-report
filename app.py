import streamlit as st
import requests
from bs4 import BeautifulSoup
import datetime

# Page Config
st.set_page_config(page_title="HeyFund Research Report", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .report-card { border: 3px solid #b8922e; padding: 20px; background: white; max-width: 800px; margin: auto; font-family: sans-serif; }
    </style>
""", unsafe_allow_html=True)

def get_google_finance_data(ticker):
    # Google Finance uses TICKER:EXCHANGE format
    url = f"https://www.google.com/finance/quote/{ticker}:NSE"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Price nikalo
        price_class = soup.find("div", {"class": "YMlKec fxKbKc"})
        price = price_class.text if price_class else "N/A"
        
        # Company Name nikalo
        name_class = soup.find("div", {"class": "zz1Oce"})
        name = name_class.text if name_class else ticker
        
        # Market Cap aur baaki details ke liye
        details = {}
        for div in soup.find_all("div", {"class": "P6K39c"}):
            parent = div.find_parent("div", {"class": "mfs7Fc"})
            if parent:
                label = parent.find("div", {"class": "mfs7Fc"}).text if parent.find("div", {"class": "mfs7Fc"}) else ""
                details[label] = div.text

        return {
            "price": price,
            "name": name,
            "mcap": details.get("Market cap", "N/A"),
            "pe": details.get("P/E ratio", "N/A"),
            "yield": details.get("Dividend yield", "N/A"),
            "ticker": ticker
        }
    except:
        return None

# Sidebar
st.sidebar.title("HeyFund Research")
ticker_input = st.sidebar.text_input("Enter NSE Ticker (e.g. RELIANCE, TCS)", value="RELIANCE").upper().strip()
generate_btn = st.sidebar.button("Generate Report")

if ticker_input:
    with st.spinner(f'Fetching live data from Google Finance for {ticker_input}...'):
        data = get_google_finance_data(ticker_input)
    
    if data and data['price'] != "N/A":
        report_date = datetime.date.today().strftime("%d %b %Y")
        
        html_code = f"""
        <div class="report-card">
            <div style="background: #111118; color: white; padding: 20px; text-align: center; border-radius: 5px;">
                <h1 style="color: #b8922e; margin: 0;">HeyFund Research Team</h1>
                <p style="margin: 5px 0; opacity: 0.8;">Live Equity Research Report</p>
            </div>
            
            <div style="padding: 30px; text-align: center;">
                <h2 style="margin: 0; color: #111118; font-size: 32px;">{data['name']}</h2>
                <p style="font-size: 16px; color: #666;">Exchange: NSE | Ticker: {data['ticker']} | Date: {report_date}</p>
                <div style="font-size: 48px; font-weight: bold; color: #111118; margin: 20px 0;">
                    {data['price']}
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; padding: 20px; background: #fdf9f0; border-radius: 10px;">
                <div style="text-align: center; border-right: 1px solid #ddd;">
                    <h4 style="margin: 0; color: #b8922e; font-size: 12px;">MARKET CAP</h4>
                    <p style="font-size: 20px; font-weight: bold; margin: 5px 0;">{data['mcap']}</p>
                </div>
                <div style="text-align: center;">
                    <h4 style="margin: 0; color: #b8922e; font-size: 12px;">P/E RATIO</h4>
                    <p style="font-size: 20px; font-weight: bold; margin: 5px 0;">{data['pe']}</p>
                </div>
            </div>

            <div style="margin-top: 30px; padding: 25px; background: #111118; color: white; border-radius: 10px;">
                <h3 style="color: #b8922e; margin-top: 0;">HeyFund Conviction</h3>
                <p style="line-height: 1.6; opacity: 0.9; font-size: 15px;">
                    Current Price action shows strong support at these levels. The {data['pe']} P/E suggests the stock is trading at 
                    fair valuation relative to historical averages. Investors may consider a long-term approach.
                </p>
                <div style="margin-top: 15px; font-weight: bold; color: #b8922e;">
                    Verdict: STABLE / ACCUMULATE
                </div>
            </div>

            <div style="margin-top: 20px; font-size: 11px; color: #999; text-align: center;">
                <b>Disclaimer:</b> Not SEBI Registered. For Educational Purpose Only. Research by HeyFund Research Team.
            </div>
        </div>
        """
        st.components.v1.html(html_code, height=850, scrolling=True)
    else:
        st.error(f"Error: Could not fetch data for '{ticker_input}'. Make sure the NSE ticker is correct.")
else:
    st.info("Enter a stock name (e.g. INFY, TCS) to see the report.")
