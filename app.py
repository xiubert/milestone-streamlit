import streamlit as st
import pandas as pd
import requests
import numpy as np
import plotly.express as px
import datetime

import os
import dotenv
from dotenv import load_dotenv
load_dotenv()

alphaAPI = os.environ.get("ALPHA_VANTAGE_API")

@st.cache
def get_tickerData(sticker,key=alphaAPI):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={sticker}&outputsize=full&apikey={key}'
    r = requests.get(url)
    sdata = r.json()

    df = pd.DataFrame.from_dict(sdata['Time Series (Daily)']).T
    df.index = pd.to_datetime(df.index)
    df['4. close'] = pd.to_numeric(df['4. close'])

    return df

@st.cache
def plotTickerMo(year, month, ticker):
    monthN=datetime.datetime.strptime(month, "%B").month
    data = df.iloc[np.logical_and(df.index.month==monthN,df.index.year==year)]

    fig = px.line(data, x=data.index, y="4. close", title=f'Daily closing prices for {ticker} in {month} of {year}',
             labels={
                     "index": "Date",
                     "4. close": "closing price (USD)"})
    return fig

sticker = st.text_input('Stock Ticker Symbol:',key="tickerInput")

if st.session_state.tickerInput == "":
    st.write("Enter a ticker symbol...")
    st.stop()

try:
    df = get_tickerData(sticker)
except:
    st.write("Invalid or unrecognized stock ticker symbol")
    st.stop()
    
yearOpts = df.index.year.unique()[::-1]

with st.form(key='yearFirst'):
    yearSel = st.selectbox(
     'choose year first:',
     tuple(yearOpts),index=0)
    
    monthOpts = df.index[df.index.year==yearSel].month_name().unique()[::-1]
    submit_year = st.form_submit_button(label='choose year')

with st.form(key='monthSecond'):
    moSel = st.selectbox(
     'choose month',
     tuple(monthOpts),index=0)
    
    submit_button = st.form_submit_button(label='Plot')

if not submit_button:
        st.stop()

st.plotly_chart(plotTickerMo(yearSel, moSel,sticker), use_container_width=True)