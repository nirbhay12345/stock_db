import nsepython as nse
import yfinance as yf # https://ranaroussi.github.io/yfinance/index.html
import streamlit as st
from models.metadata import StockMetaData

@st.cache_data
def get_stock_data(symbol, start_date, end_date):

    stock_data = yf.download(f'{symbol}', start = start_date, end = end_date) 

    stock_data = stock_data[["Open", "High", "Low", "Close", "Volume"]]
    stock_data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

    return stock_data.sort_index(ascending=False)

def get_stock_list():

    all_stocks = nse.nse_eq_symbols()
    stock_list = [f'{i}.NS' for i in all_stocks]
    return stock_list

def get_stock_metadata(symbol):

    metadata = yf.Ticker(symbol)
    stock_md = StockMetaData(**metadata.info)

    return stock_md