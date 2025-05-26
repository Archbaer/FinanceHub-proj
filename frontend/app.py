import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json

st.set_page_config(
    page_title="FinanceHub",
    page_icon="📈", 
    layout="wide"
)

API_BASE_URL = "http://backend:8000/api"

def apply_dark_theme():
    st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #fafafa; }
    .stSidebar { background-color: #262730; }
    .stButton > button { background-color: #0052cc; color: #fafafa; }
    .stMetric { background-color: #262730; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

def apply_light_theme():
    st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #262730; }
    </style>
    """, unsafe_allow_html=True)

if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

if 'page' not in st.session_state:
    st.session_state.page = "home"

if 'search_history' not in st.session_state:
    st.session_state.search_history = []

if st.session_state.dark_mode:
    apply_dark_theme()
else:
    apply_light_theme()

def add_to_history(symbol):
    if symbol in st.session_state.search_history:
        st.session_state.search_history.remove(symbol)
    st.session_state.search_history.insert(0, symbol)
    if len(st.session_state.search_history) > 10:
        st.session_state.search_history = st.session_state.search_history[:10]

def fetch_stock_data(symbol, period="1y"):
    try:
        response = requests.get(f"{API_BASE_URL}/stock/{symbol}?period={period}")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def fetch_trending_stocks():
    try:
        response = requests.get(f"{API_BASE_URL}/trending/stocks")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def render_sidebar():
    with st.sidebar:
        st.title("🏠 FinanceHub")
        
        if st.button("🌙 Dark" if not st.session_state.dark_mode else "☀️ Light"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
        
        st.markdown("---")
        
        pages = {
            "🏠 Home": "home",
            "📊 Stocks": "stocks", 
            "₿ Crypto": "crypto",
            "💼 Portfolio": "portfolio"
        }

        # Use radio for navigation
        selected = st.radio(
            "Navigation",
            list(pages.keys()),
            index=list(pages.values()).index(st.session_state.page),
            label_visibility="collapsed"
        )
        st.session_state.page = pages[selected]
        
        if st.session_state.page in ["stocks", "crypto"]:
            st.markdown("---")
            symbol = st.text_input("Quick Search", placeholder="AAPL, TSLA...")
            
            if st.button("Search", type="primary"):
                if symbol:
                    add_to_history(symbol.upper())
                    st.session_state.current_symbol = symbol.upper()
                    st.rerun()
        
        if st.session_state.search_history:
            st.markdown("#### Recent")
            for sym in st.session_state.search_history[:5]:
                if st.button(sym, key=f"hist_{sym}"):
                    st.session_state.current_symbol = sym
                    st.session_state.page = "stocks"
                    st.rerun()

render_sidebar()

if st.session_state.page == "home":
    st.title("📈 FinanceHub")
    st.markdown("### Your Trading Dashboard")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 🔥 Trending Stocks")
        trending = fetch_trending_stocks()
        
        if trending:
            for stock in trending:
                col_sym, col_price, col_change = st.columns([1, 1, 1])
                with col_sym:
                    if st.button(stock['symbol'], key=f"trend_{stock['symbol']}"):
                        st.session_state.current_symbol = stock['symbol']
                        st.session_state.page = "stocks"
                        st.rerun()
                with col_price:
                    st.write(f"${stock['price']:.2f}")
                with col_change:
                    color = "🟢" if stock['change'] >= 0 else "🔴"
                    st.write(f"{color} {stock['change']:.2f}%")
    
    with col2:
        st.markdown("#### 🚀 Quick Actions")
        
        if st.button("📊 Analyze Stocks", type="primary", use_container_width=True):
            st.session_state.page = "stocks"
            st.rerun()
        
        if st.button("₿ Crypto Analysis", use_container_width=True):
            st.session_state.page = "crypto"
            st.rerun()

elif st.session_state.page == "stocks":
    st.title("📊 Stock Analysis")
    
    if 'current_symbol' in st.session_state:
        symbol = st.session_state.current_symbol
        
        with st.spinner(f"Loading {symbol}..."):
            stock_data = fetch_stock_data(symbol)
            
            if stock_data:
                data = stock_data['data']
                info = stock_data['info']
                
                if data:
                    df = pd.DataFrame(data)
                    df['Date'] = pd.to_datetime(df['Date'])
                    
                    current_price = df['Close'].iloc[-1]
                    prev_price = df['Close'].iloc[-2] if len(df) > 1 else current_price
                    change = current_price - prev_price
                    pct_change = (change / prev_price) * 100
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Price", f"${current_price:.2f}")
                    with col2:
                        st.metric("Change", f"${change:.2f}")
                    with col3:
                        st.metric("Change %", f"{pct_change:+.2f}%")
                    with col4:
                        volume = df['Volume'].iloc[-1]
                        st.metric("Volume", f"{volume:,}")
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df['Date'],
                        y=df['Close'],
                        mode='lines',
                        name=symbol,
                        line=dict(color='#0052cc', width=2)
                    ))
                    
                    fig.update_layout(
                        title=f'{symbol} Stock Price',
                        xaxis_title='Date',
                        yaxis_title='Price ($)',
                        template='plotly_white',
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    if info:
                        st.subheader("Company Info")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Company:** {info.get('longName', 'N/A')}")
                            st.write(f"**Sector:** {info.get('sector', 'N/A')}")
                        with col2:
                            market_cap = info.get('marketCap', 0)
                            if market_cap >= 1e12:
                                st.write(f"**Market Cap:** ${market_cap/1e12:.2f}T")
                            elif market_cap >= 1e9:
                                st.write(f"**Market Cap:** ${market_cap/1e9:.2f}B")
                            else:
                                st.write(f"**Market Cap:** ${market_cap/1e6:.2f}M")
            else:
                st.error(f"Could not load data for {symbol}")
    else:
        st.info("Enter a stock symbol to get started!")

elif st.session_state.page == "crypto":
    st.title("₿ Cryptocurrency Analysis")
    
    popular_cryptos = ['BTC', 'ETH', 'SOL', 'ADA', 'DOT']
    
    st.subheader("Popular Cryptocurrencies")
    cols = st.columns(5)
    
    for i, crypto in enumerate(popular_cryptos):
        with cols[i]:
            if st.button(crypto, key=f"crypto_{crypto}"):
                st.session_state.current_symbol = f"{crypto}-USD"
                st.rerun()

elif st.session_state.page == "portfolio":
    st.title("💼 Portfolio Management")
    st.info("Portfolio features coming soon!")

st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h4>FinanceHub</h4>
    <p>Built with ❤️ | Data by Yahoo Finance</p>
    <a href='https://github.com/archbaer' target='_blank'> GitHub</a>
</div>
""", unsafe_allow_html=True)