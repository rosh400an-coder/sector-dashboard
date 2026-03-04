import streamlit as st
import yfinance as yf
import pandas as pd
import pytz
from datetime import datetime

st.set_page_config(layout="wide")

# ---------------- FIXED SECTOR MAP ----------------
sector_map = {
'Industrials': ['BHEL.NS','CUMMINSIND.NS','INDIGO.NS','KPIL.NS','SUPREMEIND.NS','ARE&M.NS','CGPOWER.NS','BDL.NS','BEL.NS','KEI.NS','COCHINSHIP.NS','BLS.NS','BEML.NS','GESHIP.NS','SRF.NS','DATAPATTNS.NS','HBLENGINE.NS','SIEMENS.NS','ASHOKLEY.NS','NCC.NS','ASTRAL.NS','POLYCAB.NS','RVNL.NS','ZENTEC.NS','LT.NS','CYIENT.NS','TRITURBINE.NS','ABB.NS','DELHIVERY.NS','POWERINDIA.NS','INOXWIND.NS','TIINDIA.NS','AFCONS.NS','BLUESTARCO.NS','IRCON.NS','HAVELLS.NS','KEC.NS','JWL.NS','KAJARIACER.NS','GMRAIRPORT.NS','MAZDOCK.NS','HAL.NS','JYOTICNC.NS','NBCC.NS','IRB.NS','CONCOR.NS','ADANIPORTS.NS','SWANCORP.NS','SUZLON.NS','GRSE.NS'],
'Financial Services': ['YESBANK.NS','ABCAPITAL.NS','SHRIRAMFIN.NS','HDFCBANK.NS','BAJAJFINSV.NS','MANAPPURAM.NS','BANDHANBNK.NS','APTUS.NS','CGCL.NS','MOTILALOFS.NS','AUBANK.NS','LICHSGFIN.NS','AADHARHFC.NS','MFSL.NS','PNB.NS','NUVAMA.NS','ICICIGI.NS','BAJAJHFL.NS','BANKINDIA.NS','POLICYBZR.NS','CHOLAFIN.NS','FEDERALBNK.NS','CANBK.NS','M&MFIN.NS','SBILIFE.NS','SBICARD.NS','PNBHOUSING.NS','INDIANB.NS','LICI.NS','LTF.NS','MCX.NS','ANGELONE.NS','POONAWALLA.NS','ANANDRATHI.NS','BANKBARODA.NS','GODIGIT.NS','MUTHOOTFIN.NS','FIVESTAR.NS','STARHEALTH.NS','JIOFIN.NS','CHOLAHLDNG.NS','KOTAKBANK.NS','ICICIBANK.NS','HDFCLIFE.NS','BAJAJHLDNG.NS','AXISBANK.NS','360ONE.NS','INDUSINDBK.NS','IIFL.NS','PFC.NS','CDSL.NS','IEX.NS','KARURVYSYA.NS','RECLTD.NS','UNIONBANK.NS','CREDITACC.NS','SBIN.NS','BAJFINANCE.NS','IDFCFIRSTB.NS','HUDCO.NS','IREDA.NS','IFCI.NS','IRFC.NS','BSE.NS','HDFCAMC.NS'],
# --- बाकी sectors नीचे वैसे ही paste करो ---
}

# --------- TIME ----------
ist = pytz.timezone("Asia/Kolkata")
now = datetime.now(ist)
time_str = now.strftime("%d-%b-%Y | %H:%M IST")

st.markdown(f"""
<div style="background:black;padding:15px;text-align:center">
<h2 style="color:white;">🚀 LIVE 300 STOCK SECTOR DASHBOARD</h2>
<h4 style="color:gold;">{time_str}</h4>
</div>
""", unsafe_allow_html=True)

# --------- SYMBOL LIST ----------
symbols = []
for stocks in sector_map.values():
    symbols.extend(stocks)

# --------- DOWNLOAD ----------
data = yf.download(symbols, period="1d", interval="1m", progress=False, threads=False)

if data.empty:
    st.error("Market data not available")
    st.stop()

close = data["Close"]

open_price = close.iloc[0]
current_price = close.iloc[-1]
day_change = ((current_price - open_price) / open_price) * 100

# --------- CALC ----------
results = []

for sector, stocks in sector_map.items():
    sector_data = day_change[stocks]
    avg = sector_data.mean()
    green = (sector_data > 0).sum()
    red = (sector_data < 0).sum()
    green_pct = (green / len(stocks)) * 100
    strength = (avg * 5) + (green_pct * 3)

    results.append([
        sector,
        round(avg,2),
        green,
        red,
        round(green_pct,1),
        round(strength,2)
    ])

df = pd.DataFrame(results, columns=[
    "Sector","Avg %","Green","Red","Green %","Strength"
]).sort_values("Strength", ascending=False)

st.dataframe(df, use_container_width=True)

st.caption("✔ 300 Stocks | Fixed Sector Mapping | Stable Cloud Version")
