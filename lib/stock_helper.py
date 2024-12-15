import nsepython as nse
import yfinance as yf  # https://ranaroussi.github.io/yfinance/index.html
import streamlit as st
from models.metadata import StockMetaData


@st.cache_data
def get_stock_data(symbol, start_date, end_date):
    """
    Fetch historical stock data for a given symbol and date range.

    This function uses the Yahoo Finance API to download historical stock data for a specific stock symbol
    over a specified date range. It filters and formats the data to include only essential columns:
    "Open", "High", "Low", "Close", and "Volume". The data is then sorted in descending order of the date
    to make the latest data appear first.

    Parameters:
    -----------
    symbol : str
        The stock symbol to fetch data for (e.g., "RELIANCE.NS").
    start_date : datetime or str
        The start date for fetching historical data.
    end_date : datetime or str
        The end date for fetching historical data.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing the historical stock data with the following columns:
        - "Open": The opening price of the stock.
        - "High": The highest price of the stock.
        - "Low": The lowest price of the stock.
        - "Close": The closing price of the stock.
        - "Volume": The trading volume for the stock.
        The DataFrame is sorted in descending order of the date.

    Notes:
    ------
    - The `yf.download` function is used to fetch data from Yahoo Finance.
    - The ".NS" suffix for symbols indicates stocks listed on the National Stock Exchange (NSE).
    - The function caches the data using `@st.cache_data` to avoid redundant API calls and improve performance.
    - Ensure that the required columns ("Open", "High", "Low", "Close", "Volume") exist in the downloaded data
      to avoid KeyErrors.

    Dependencies:
    -------------
    - `yfinance` library: Used for downloading stock data.
    - `streamlit.cache_data`: Used for caching the data to optimize performance in Streamlit applications.
    """
    stock_data = yf.download(f"{symbol}", start=start_date, end=end_date)

    stock_data = stock_data[["Open", "High", "Low", "Close", "Volume"]]
    stock_data.columns = ["Open", "High", "Low", "Close", "Volume"]

    return stock_data.sort_index(ascending=False)


@st.cache_data
def get_stock_list():
    """
    Retrieve a list of stock symbols for equities listed on the NSE (National Stock Exchange).

    This function fetches all available stock symbols using the `nse_eq_symbols` function
    from the `nse` module and appends the ".NS" suffix to each symbol to format them
    for use in stock market APIs or dashboards.

    Returns:
    --------
    list of str
        A list of stock symbols formatted as "{symbol}.NS".

    Notes:
    ------
    - The `nse_eq_symbols` function is expected to return a list of stock symbols
      as strings, representing equities traded on the NSE.
    - The ".NS" suffix is commonly used to indicate National Stock Exchange symbols
      when working with APIs like Yahoo Finance or similar services.
    - Ensure that the `nse` module is properly installed and configured for this function to work.

    Dependencies:
    -------------
    - `nse.nse_eq_symbols`: A method from the `nse` module that retrieves all equity symbols.
    - `streamlit.cache_data`: Used for caching the data to optimize performance in Streamlit applications.
    """
    all_stocks = nse.nse_eq_symbols()
    stock_list = [f"{i}.NS" for i in all_stocks]
    return stock_list


def get_stock_metadata(symbol):
    """
    Fetch metadata for a specific stock symbol.

    This function retrieves detailed metadata for a given stock symbol using the Yahoo Finance API.
    It uses the `Ticker` class from the `yfinance` library to fetch the metadata, and the response
    is mapped to a `StockMetaData` object for structured access and validation.

    Parameters:
    -----------
    symbol : str
        The stock symbol for which to fetch metadata (e.g., "RELIANCE.NS").

    Returns:
    --------
    StockMetaData
        An instance of the `StockMetaData` dataclass containing the stock's metadata, including:
        - `uuid`: Unique identifier for the stock.
        - `currentPrice`: Current trading price of the stock.
        - `fiftyTwoWeekLow`: Lowest price in the last 52 weeks.
        - `fiftyTwoWeekHigh`: Highest price in the last 52 weeks.
        - `trailingPE`: Price-to-Earnings ratio.
        - Additional optional attributes, such as `longName`, `symbol`, `industry`, `sector`, and more.

    Notes:
    ------
    - The function expects the `metadata.info` dictionary from Yahoo Finance to contain all required fields
      defined in the `StockMetaData` dataclass.
    - If any required field is missing, an exception may be raised during the creation of the `StockMetaData` object.
    - Ensure that the `yfinance` library is properly installed and the `StockMetaData` dataclass is correctly defined
      and imported.

    Dependencies:
    -------------
    - `yfinance.Ticker`: Fetches stock metadata from Yahoo Finance.
    - `StockMetaData`: A dataclass used to validate and structure the metadata.

    """
    metadata = yf.Ticker(symbol)
    stock_md = StockMetaData(**metadata.info)
    return stock_md
