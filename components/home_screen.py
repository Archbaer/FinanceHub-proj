import streamlit as st
import pandas as pd
from utils.data_fetcher import StockDataFetcher
from utils.crypto_fetcher import CryptoDataFetcher

def render_home_screen():
    st.title("📈 FinanceHub - Your Trading Dashboard")
    
    st.markdown("""
    ### Welcome to FinanceHub
    Your comprehensive platform for stock and cryptocurrency analysis. Track markets, 
    build portfolios, and make informed investment decisions.
    """)
    
    # Popular stocks section with charts
    st.markdown("#### 🔥 Top 3 Most Popular Stocks")
    
    popular_stocks = ['AAPL', 'TSLA', 'NVDA']
    
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]
    
    data_fetcher = StockDataFetcher()
    
    for i, symbol in enumerate(popular_stocks):
        with columns[i]:
            try:
                data = data_fetcher.get_stock_data(symbol, "1mo")
                if data is not None and not data.empty:
                    current_price = data['Close'].iloc[-1]
                    prev_price = data['Close'].iloc[-2] if len(data) > 1 else current_price
                    change = current_price - prev_price
                    pct_change = (change / prev_price) * 100
                    
                    st.subheader(f"{symbol}")
                    st.metric(
                        "Price", 
                        f"${current_price:.2f}",
                        f"{change:+.2f} ({pct_change:+.2f}%)"
                    )
                    
                    # Create mini chart
                    import plotly.graph_objects as go
                    fig = go.Figure()
                    
                    color = '#00875A' if pct_change >= 0 else '#DE350B'
                    
                    fig.add_trace(go.Scatter(
                        x=data['Date'],
                        y=data['Close'],
                        mode='lines',
                        line=dict(color=color, width=2),
                        showlegend=False
                    ))
                    
                    fig.update_layout(
                        height=200,
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis=dict(visible=False),
                        yaxis=dict(visible=False),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    if st.button(f"Analyze {symbol}", key=f"analyze_{symbol}", use_container_width=True):
                        st.session_state.current_symbol = symbol
                        st.session_state.page = "stocks"
                        st.rerun()
                else:
                    st.error(f"Could not load {symbol}")
            except Exception as e:
                st.error(f"Error loading {symbol}")
    
    st.markdown("---")
    
    # Quick actions and trending section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 🔥 Trending Today")
        
        trending_stocks = ['AAPL', 'TSLA', 'NVDA', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NFLX']
        trending_cryptos = ['BTC-USD', 'ETH-USD', 'SOL-USD']
        
        tabs = st.tabs(["🏢 Stocks", "₿ Crypto"])
        
        with tabs[0]:
            render_trending_stocks(trending_stocks)
        
        with tabs[1]:
            render_trending_crypto(trending_cryptos)
    
    with col2:
        st.markdown("#### 🚀 Quick Actions")
        
        if st.button("📊 Analyze Stocks", type="primary", use_container_width=True):
            st.session_state.page = "stocks"
            st.rerun()
        
        if st.button("₿ Crypto Analysis", use_container_width=True):
            st.session_state.page = "crypto"
            st.rerun()
        
        if st.button("📈 Market Overview", use_container_width=True):
            st.session_state.page = "market"
            st.rerun()
        
        st.markdown("---")
        
        if 'search_history' in st.session_state and st.session_state.search_history:
            st.markdown("#### 🕒 Recent Searches")
            for symbol in st.session_state.search_history[:5]:
                if st.button(symbol, key=f"recent_{symbol}", use_container_width=True):
                    st.session_state.quick_symbol = symbol
                    st.session_state.page = "stocks"
                    st.rerun()

def render_trending_stocks(symbols):
    data_fetcher = StockDataFetcher()
    trending_data = []
    
    for symbol in symbols:
        try:
            data = data_fetcher.get_stock_data(symbol, "5d")
            if data is not None and not data.empty:
                current = data['Close'].iloc[-1]
                prev = data['Close'].iloc[-2] if len(data) > 1 else current
                change = ((current - prev) / prev) * 100
                
                trending_data.append({
                    'Symbol': symbol,
                    'Price': f"${current:.2f}",
                    'Change': f"{change:+.2f}%"
                })
        except:
            pass
    
    if trending_data:
        df = pd.DataFrame(trending_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

def render_trending_crypto(symbols):
    crypto_fetcher = CryptoDataFetcher()
    crypto_data = []
    
    for symbol in symbols:
        try:
            data = crypto_fetcher.get_crypto_data(symbol, "5d")
            if data is not None and not data.empty:
                current = data['Close'].iloc[-1]
                prev = data['Close'].iloc[-2] if len(data) > 1 else current
                change = ((current - prev) / prev) * 100
                
                name = symbol.replace('-USD', '')
                crypto_data.append({
                    'Crypto': name,
                    'Price': f"${current:,.2f}",
                    'Change': f"{change:+.2f}%"
                })
        except:
            pass
    
    if crypto_data:
        df = pd.DataFrame(crypto_data)
        st.dataframe(df, use_container_width=True, hide_index=True)