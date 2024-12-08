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
    stocklist = [f'{i}.NS' for i in all_stocks]
    return stocklist

def get_stock_metadata(symbol):

    metadata = yf.Ticker(symbol)
    stock_md = StockMetaData(
                uuid=metadata.info['uuid'],
                currentPrice=metadata.info['currentPrice'], 
                longName=metadata.info['longName'], 
                symbol=metadata.info['symbol'], 
                fiftyTwoWeekLow=metadata.info['fiftyTwoWeekLow'], 
                fiftyTwoWeekHigh=metadata.info['fiftyTwoWeekHigh'], 
                trailingPE=metadata.info['trailingPE'], 
                longBusinessSummary=metadata.info['longBusinessSummary'], 
                industry=metadata.info['industry'], 
                industryKey=metadata.info['industryKey'], 
                sector=metadata.info['sector'], 
                sectorKey=metadata.info['sectorKey']
            )

    return stock_md