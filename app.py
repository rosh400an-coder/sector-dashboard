
import streamlit as st
import yfinance as yf
import pandas as pd
import pytz
from datetime import datetime

st.set_page_config(layout="wide")

# ---------- SECTOR MAP ----------
sector_map = {
    "Technology": ["TCS.NS","INFY.NS","WIPRO.NS"],
    "Banking": ["HDFCBANK.NS","ICICIBANK.NS","SBIN.NS"],
    "Energy": ["RELIANCE.NS","ONGC.NS","BPCL.NS"]
}

symbols = []
for stocks in sector_map.values():
    symbols.extend(stocks)

# ---------- TIME ----------
ist = pytz.timezone("Asia/Kolkata")
now = datetime.now(ist)
time_str = now.strftime("%d-%b-%Y | %H:%M IST")

st.markdown(
    f"""
    <div style="background:black;padding:15px;text-align:center">
        <h2 style="color:white;">🚀 LIVE SECTOR DASHBOARD</h2>
        <h4 style="color:gold;">{time_str}</h4>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- DATA ----------
try:
    data = yf.download(
        symbols,
        period="1d",
        interval="1m",
        progress=False,
        threads=False
    )
except:
    st.error("Data download error")
    st.stop()

if data.empty:
    st.error("Market Data Not Available")
    st.stop()

if isinstance(data.columns, pd.MultiIndex):
    close = data["Close"]
else:
    close = data["Close"]

if close.empty:
    st.error("Market Closed")
    st.stop()

open_price = close.iloc[0]
current_price = close.iloc[-1]
day_change = ((current_price - open_price) / open_price) * 100

# ---------- SECTOR CALC ----------
results = []

for sector, stock_list in sector_map.items():
    valid = [s for s in stock_list if s in day_change.index]
    if len(valid) == 0:
        continue

    sector_change = day_change[valid]
    sector_avg = sector_change.mean()

    green = (sector_change > 0).sum()
    red = (sector_change < 0).sum()

    results.append([
        sector,
        round(sector_avg,2),
        green,
        red
    ])

df = pd.DataFrame(results, columns=["Sector","Avg %","Green","Red"])
df = df.sort_values("Avg %", ascending=False).reset_index(drop=True)

st.dataframe(df, use_container_width=True)

st.caption("🔄 Data updates automatically on page refresh")
