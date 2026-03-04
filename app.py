import streamlit as st
import yfinance as yf
import pandas as pd
import pytz
from datetime import datetime
import time

st.set_page_config(layout="wide")

# ---------------- SECTOR MAP ----------------
sector_map = {
    "Technology": ["TCS.NS", "INFY.NS", "WIPRO.NS"],
    "Banking": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS"],
    "Energy": ["RELIANCE.NS", "ONGC.NS", "BPCL.NS"]
}

# ---------------- LIVE CLOCK (NO FLIP) ----------------
st.markdown("""
<div style="text-align:center">
<h1>🚀 LIVE SECTOR DASHBOARD</h1>
<h3 id="clock" style="color:#FFD700;"></h3>
</div>

<script>
function updateClock() {
    const now = new Date();
    const options = { 
        timeZone: 'Asia/Kolkata',
        year: 'numeric', 
        month: 'short', 
        day: '2-digit',
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit'
    };
    document.getElementById("clock").innerHTML =
        now.toLocaleString("en-IN", options) + " IST";
}
setInterval(updateClock, 1000);
updateClock();
</script>
""", unsafe_allow_html=True)

# ---------------- MINUTE SYNC LOGIC ----------------
ist = pytz.timezone("Asia/Kolkata")
now = datetime.now(ist)

if "last_minute" not in st.session_state:
    st.session_state.last_minute = -1
    st.session_state.cached_df = pd.DataFrame()

if now.minute != st.session_state.last_minute:

    symbols = []
    for stocks in sector_map.values():
        symbols.extend(stocks)

    data = yf.download(
        symbols,
        period="1d",
        interval="1m",
        progress=False,
        threads=False
    )

    if not data.empty:

        close = data["Close"]

        # LAST CLOSED CANDLE
        last_close = close.iloc[-2]
        prev_close = close.iloc[-3]

        pct_change = ((last_close - prev_close) / prev_close) * 100

        results = []

        for sector, stocks in sector_map.items():
            sector_data = pct_change[stocks]
            avg = sector_data.mean()
            green = (sector_data > 0).sum()
            red = (sector_data < 0).sum()

            results.append({
                "Sector": sector,
                "Avg %": round(avg, 2),
                "Green": int(green),
                "Red": int(red)
            })

        df = pd.DataFrame(results).sort_values("Avg %", ascending=False)

        st.session_state.cached_df = df
        st.session_state.last_minute = now.minute

# ---------------- DISPLAY TABLE ----------------
if not st.session_state.cached_df.empty:
    st.dataframe(
        st.session_state.cached_df,
        use_container_width=True
    )

st.caption("✔ Data updates automatically every new minute (last closed candle)")
