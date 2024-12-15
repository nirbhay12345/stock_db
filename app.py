import datetime
from dateutil.relativedelta import relativedelta
import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
from lib import stock_helper as sh

@st.cache_resource
def charts(stock_data, chart_type="Line"):
    if chart_type == "Candle":
        # candlestick chart
        candlestick_chart = go.Figure(data=[go.Candlestick(x=stock_data.index, open=stock_data['Open'], high=stock_data['High'], low=stock_data['Low'], close=stock_data['Close'])])
        candlestick_chart.update_layout(xaxis_rangeslider_visible=False)
        chart = candlestick_chart
    elif chart_type == "Area":
        barchart = px.area(stock_data, x=stock_data.index, y=stock_data['High'])
        chart = barchart
    else:
        # line chart
        linechart = go.Figure([go.Scatter(x=stock_data.index, y=stock_data['High'])])
        chart = linechart

    return chart

def calculate_price_difference(stock_data):
    latest_price = stock_data.iloc[0]["Close"]
    previous_year_price = stock_data.iloc[252]["Close"] if len(stock_data) > 252 else stock_data.iloc[-1]["Close"]
    price_difference = latest_price - previous_year_price
    percentage_difference = (price_difference / previous_year_price) * 100
    return price_difference, percentage_difference

def app():
    st.set_page_config(page_title="Stock Dashboard", layout="wide", page_icon="📈")
    hide_menu_style = "<style> footer {visibility: hidden;} </style>"
    st.markdown(hide_menu_style, unsafe_allow_html=True)
    
    st.title("📈 Stock Dashboard")
    symbols = sh.get_stock_list()
    symbol = st.sidebar.selectbox("Select a stock symbol:", symbols, index=20)
    
    start_date = st.sidebar.date_input("Start Date", datetime.datetime.now() - relativedelta(year=2023))
    end_date = st.sidebar.date_input("End Date", datetime.datetime.now())

    if symbol:
        stock_data = sh.get_stock_data(symbol, start_date, end_date)
        metadata = sh.get_stock_metadata(symbol)
        if stock_data is not None:
            st.sidebar.text(f"Stock: {metadata.longName}")
            st.sidebar.text(f"Sector: {metadata.sector}")
            st.sidebar.text(f"Website: {metadata.website}")
            price_difference, percentage_difference = calculate_price_difference(stock_data)

            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Close Price", f"₹{metadata.currentPrice:.2f}")
            with col2:
                st.metric("Price Difference", f"₹{price_difference:.2f}", f"{percentage_difference:+.2f}%")
                pass
            with col3:
                st.metric("52-Week High", f"₹{metadata.fiftyTwoWeekHigh:.2f}")
            with col4:
                st.metric("52-Week Low", f"₹{metadata.fiftyTwoWeekLow:.2f}")
            with col5:
                st.metric("PE Ratio", f"{metadata.trailingPE:.2f}")

            st.subheader("Trend Chart")
            chart_type = st.pills("Type", options=["Line", "Candle", "Area"], default="Line", label_visibility="collapsed")
            st.plotly_chart(charts(stock_data, chart_type), use_container_width=True)

            st.subheader("Summary")
            st.dataframe(stock_data, use_container_width=True)

            st.download_button("Download Stock Data Overview", stock_data.to_csv(index=True), file_name=f"{symbol}_stock_data.csv", mime="text/csv")

if __name__ == "__main__":
    app()