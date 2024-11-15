import streamlit as st
from utils import StockFetch

# Setting page title and icon
st.set_page_config(page_title="Stock App", page_icon="📉", layout="wide")


@st.cache_resource
def get_stock_client(api_key):
    return StockFetch(api_key=api_key)


# Setup api key
api_key = st.secrets["API_KEY"]
client = get_stock_client(api_key)


@st.cache_data(ttl=3600)
def search_stock(company):
    return client.symbol_search(company)


@st.cache_data(ttl=3600)
def plot_chart(symbol):
    return client.plot_chart(symbol)


if __name__ == "__main__":
    # Title of my application
    st.title("Stock Market application")

    # Take company name as input from user
    company = st.text_input("Please enter company name :")

    # Add dropdown for company symbols
    if company:
        search_data = search_stock(company)
        if search_data:
            options = st.selectbox("Enter the company symbol", list(search_data.keys()))
            symbol_data = search_data.get(options)
            st.success(f"Company Name : {symbol_data[0]}")
            st.success(f"Type : {symbol_data[1]}")
            st.success(f"Region : {symbol_data[2]}")

            if st.button("submit"):
                fig = plot_chart(symbol=options)
                st.plotly_chart(fig)

        else:
            st.error(f"Company Name not found")
