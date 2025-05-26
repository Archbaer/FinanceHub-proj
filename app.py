import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import io

from utils.data_fetcher import StockDataFetcher
from utils.chart_generator import ChartGenerator
from utils.metrics_calculator import MetricsCalculator
from utils.cache_manager import CacheManager
from utils.crypto_fetcher import CryptoDataFetcher
from utils.data_exporter import DataExporter
from components.home_screen import render_home_screen
from components.footer import render_footer

st.set_page_config(
    page_title="FinanceHub - Trading Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def get_components():
    return StockDataFetcher(), ChartGenerator(), MetricsCalculator(), CacheManager(), CryptoDataFetcher(), DataExporter()

data_fetcher, chart_generator, metrics_calculator, cache_manager, crypto_fetcher, data_exporter = get_components()

if 'page' not in st.session_state:
    st.session_state.page = "home"

if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Apply theme
if st.session_state.dark_mode:
    st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stMarkdown {
        color: #ffffff;
    }
    .stButton > button {
        background-color: #0052cc;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# Professional Website Navigation
st.markdown("""
<style>
/* Hide Streamlit's default header and padding */
#MainMenu {visibility: hidden;}
.stDeployButton {display:none;}
footer {visibility: hidden;}
.stApp > header {visibility: hidden;}

/* Remove top padding from main container */
.main .block-container {
    padding-top: 0rem;
    padding-bottom: 0rem;
    max-width: none;
}

/* Custom navbar styles */
.main-nav {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-bottom: 3px solid rgba(255,255,255,0.1);
    padding: 1rem 0;
    margin: -1rem -1rem 2rem -1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    position: sticky;
    top: 0;
    z-index: 1000;
    backdrop-filter: blur(10px);
}

.main-nav.dark-mode {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border-bottom: 3px solid rgba(102, 126, 234, 0.3);
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.nav-brand {
    font-size: 1.8rem;
    font-weight: 800;
    color: white !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.nav-links {
    display: flex;
    gap: 0.5rem;
    align-items: center;
}

/* Enhanced button styles */
.nav-btn {
    background: rgba(255,255,255,0.1) !important;
    border: 2px solid rgba(255,255,255,0.2) !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 25px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    backdrop-filter: blur(5px) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    font-size: 0.85rem !important;
    position: relative !important;
    overflow: hidden !important;
}

.nav-btn:hover {
    background: rgba(255,255,255,0.25) !important;
    border-color: rgba(255,255,255,0.4) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2) !important;
    color: white !important;
}

.nav-btn:active {
    transform: translateY(0px) !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
}

/* Active page indicator */
.nav-btn.active {
    background: rgba(255,255,255,0.3) !important;
    border-color: rgba(255,255,255,0.5) !important;
    box-shadow: 0 0 20px rgba(255,255,255,0.3) !important;
}

/* Dark mode toggle special styling */
.theme-toggle {
    background: rgba(255,255,255,0.15) !important;
    border: 2px solid rgba(255,255,255,0.3) !important;
    border-radius: 50% !important;
    width: 50px !important;
    height: 50px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 1.2rem !important;
    transition: all 0.3s ease !important;
}

.theme-toggle:hover {
    background: rgba(255,255,255,0.25) !important;
    transform: rotate(180deg) scale(1.1) !important;
    box-shadow: 0 0 20px rgba(255,255,255,0.3) !important;
}

/* Responsive design */
@media (max-width: 768px) {
    .nav-container {
        flex-direction: column;
        gap: 1rem;
        padding: 0 1rem;
    }
    
    .nav-links {
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .nav-btn {
        padding: 0.5rem 1rem !important;
        font-size: 0.8rem !important;
    }
}

/* Hover effect animation */
.nav-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s;
}

.nav-btn:hover::before {
    left: 100%;
}
</style>
""", unsafe_allow_html=True)

# Apply dark mode class if needed
nav_class = "main-nav dark-mode" if st.session_state.dark_mode else "main-nav"

# Create the navbar container
st.markdown(f'''
<div class="{nav_class}">
    <div class="nav-container">
        <div class="nav-brand">
            📈 FinanceHub
        </div>
        <div class="nav-links">
            <!-- Navigation buttons will be inserted here -->
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# Navigation layout inside the navbar
nav_cols = st.columns([1, 1, 1, 1, 1, 1, 0.8])

pages = [
    ("Home", "home", "🏠"),
    ("Stock Analysis", "stocks", "📊"),
    ("Crypto Analysis", "crypto", "₿"),
    ("Market Overview", "market", "📈"),
    ("Portfolio", "portfolio", "💼"),
    ("Settings", "settings", "⚙️")
]

for i, (label, page_key, icon) in enumerate(pages):
    with nav_cols[i]:
        # Add active class if current page
        button_class = "nav-btn active" if st.session_state.page == page_key else "nav-btn"
        
        if st.button(f"{icon} {label}", key=f"nav_{page_key}", use_container_width=True):
            st.session_state.page = page_key
            st.rerun()


with nav_cols[6]:
    toggle_icon = "🌙" if not st.session_state.dark_mode else "☀️"
    if st.button(toggle_icon, key="theme_toggle", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Close navbar container
st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

# Main content container
st.markdown('<div class="main-container" style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;">', unsafe_allow_html=True)

# Sidebar for search (only on relevant pages)
if st.session_state.page in ["stocks", "crypto"]:
    with st.sidebar:
        st.subheader("Quick Search")
        
        symbol_input = st.text_input(
            "Enter Symbol",
            placeholder="AAPL, BTC-USD...",
            key="quick_search"
        )
        
        period_options = {
            "1 Week": "1wk",
            "1 Month": "1mo", 
            "3 Months": "3mo",
            "6 Months": "6mo",
            "1 Year": "1y",
            "2 Years": "2y",
            "5 Years": "5y"
        }
        
        period = st.selectbox("Time Period", options=list(period_options.keys()), index=4)
        
        if st.button("Search", type="primary", use_container_width=True):
            if symbol_input:
                cache_manager.add_to_search_history(symbol_input)
                st.session_state.current_symbol = symbol_input.upper()
                st.session_state.current_period = period_options[period]
                st.rerun()
    
    history = cache_manager.get_search_history()
    if history:
        with st.sidebar:
            st.markdown("#### Recent Searches")
            for symbol in history[:5]:
                if st.button(f"📊 {symbol}", key=f"hist_{symbol}", use_container_width=True):
                    st.session_state.current_symbol = symbol
                    st.session_state.page = "stocks"
                    st.rerun()

# Page content
if st.session_state.page == "home":
    render_home_screen()

elif st.session_state.page == "stocks":
    st.title("📊 Stock Analysis")
    
    if 'current_symbol' in st.session_state:
        symbol = st.session_state.current_symbol
        period = st.session_state.get('current_period', '1y')
        
        with st.spinner(f"Loading data for {symbol}..."):
            data = data_fetcher.get_stock_data(symbol, period)
            info = data_fetcher.get_stock_info(symbol)
            
            if data is not None and not data.empty:
                tabs = st.tabs(["📈 Charts", "📊 Metrics", "📋 Details", "📥 Export Data"])
                
                with tabs[0]:
                    fig = chart_generator.create_candlestick_chart(data, symbol)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    vol_fig = chart_generator.create_volume_chart(data, symbol)
                    st.plotly_chart(vol_fig, use_container_width=True)
                
                with tabs[1]:
                    metrics = metrics_calculator.calculate_metrics(data, info)
                    if metrics:
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Current Price", f"${metrics.get('Current Price', 0):.2f}")
                        with col2:
                            change = metrics.get('Price Change', 0)
                            st.metric("Price Change", f"${change:.2f}")
                        with col3:
                            pct_change = metrics.get('Percent Change', 0)
                            st.metric("Change %", f"{pct_change:.2f}%")
                        with col4:
                            volume = metrics.get('Volume', 0)
                            st.metric("Volume", f"{volume:,}")
                
                with tabs[2]:
                    if info:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Company:** {info.get('longName', 'N/A')}")
                            st.write(f"**Sector:** {info.get('sector', 'N/A')}")
                            st.write(f"**Industry:** {info.get('industry', 'N/A')}")
                        with col2:
                            market_cap = info.get('marketCap', 0)
                            if market_cap >= 1e12:
                                st.write(f"**Market Cap:** ${market_cap/1e12:.2f}T")
                            elif market_cap >= 1e9:
                                st.write(f"**Market Cap:** ${market_cap/1e9:.2f}B")
                            else:
                                st.write(f"**Market Cap:** ${market_cap/1e6:.2f}M")
                            
                            pe_ratio = info.get('trailingPE', 'N/A')
                            st.write(f"**P/E Ratio:** {pe_ratio}")
                
                with tabs[3]:
                    st.subheader("📥 Download Complete Historical Data")
                    st.markdown(f"**Export complete daily data for {symbol}**")
                    st.markdown("Get every single trading day with OHLC prices, volume, moving averages, volatility, and technical indicators.")
                    
                    export_period_options = {
                        "1 Month": "1mo",
                        "3 Months": "3mo", 
                        "6 Months": "6mo",
                        "1 Year": "1y",
                        "2 Years": "2y",
                        "5 Years": "5y",
                        "Max": "max"
                    }
                    
                    export_period = st.selectbox("Select Export Period", options=list(export_period_options.keys()), index=3)
                    
                    if st.button("📊 Generate Complete Dataset", type="primary"):
                        with st.spinner("Generating comprehensive dataset..."):
                            csv_data = data_exporter.export_stock_historical_data(symbol, export_period_options[export_period])
                            
                            if csv_data:
                                st.download_button(
                                    label="📥 Download Complete Historical Data (CSV)",
                                    data=csv_data,
                                    file_name=f"{symbol}_complete_data_{export_period_options[export_period]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    mime="text/csv"
                                )
                                st.success(f"✅ Complete dataset ready! Contains daily data for {export_period}")
                                st.info("📊 Dataset includes: OHLC prices, volume, daily returns, moving averages (7, 20, 50 days), volatility metrics, and volume analysis")
                            else:
                                st.error("Failed to generate dataset")
            else:
                st.error(f"Could not load data for {symbol}")
    else:
        st.info("Enter a stock symbol in the sidebar to get started!")

elif st.session_state.page == "crypto":
    st.title("₿ Cryptocurrency Analysis")
    
    popular_cryptos = crypto_fetcher.get_popular_cryptos()
    
    st.subheader("Popular Cryptocurrencies")
    
    crypto_cols = st.columns(5)
    for i, (symbol, name) in enumerate(list(popular_cryptos.items())[:5]):
        with crypto_cols[i]:
            if st.button(f"{name}\n{symbol.replace('-USD', '')}", key=f"crypto_{symbol}"):
                st.session_state.current_symbol = symbol
                st.rerun()
    
    if 'current_symbol' in st.session_state and st.session_state.current_symbol.endswith('-USD'):
        symbol = st.session_state.current_symbol
        
        with st.spinner(f"Loading crypto data for {symbol}..."):
            data = crypto_fetcher.get_crypto_data(symbol, "1y")
            
            if data is not None and not data.empty:
                current_price = data['Close'].iloc[-1]
                prev_price = data['Close'].iloc[-2] if len(data) > 1 else current_price
                price_change = current_price - prev_price
                pct_change = (price_change / prev_price) * 100
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Price", f"${current_price:,.2f}")
                with col2:
                    st.metric("24h Change", f"${price_change:,.2f}")
                with col3:
                    st.metric("24h Change %", f"{pct_change:+.2f}%")
                
                fig = chart_generator.create_line_chart(data, symbol.replace('-USD', ''))
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("📥 Export Crypto Data")
                if st.button("📊 Download Crypto Dataset", type="primary"):
                    csv_data = data_exporter.export_crypto_data(symbol, "1y")
                    if csv_data:
                        st.download_button(
                            label="📥 Download Crypto Data (CSV)", 
                            data=csv_data,
                            file_name=f"{symbol}_crypto_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
            else:
                st.error(f"Could not load data for {symbol}")

elif st.session_state.page == "market":
    st.title("📈 Market Overview")
    
    st.subheader("Market Indices")
    
    indices = {
        '^GSPC': 'S&P 500',
        '^DJI': 'Dow Jones',
        '^IXIC': 'NASDAQ',
        '^RUT': 'Russell 2000'
    }
    
    index_data = []
    for symbol, name in indices.items():
        try:
            data = data_fetcher.get_stock_data(symbol, "5d")
            if data is not None and not data.empty:
                current = data['Close'].iloc[-1]
                prev = data['Close'].iloc[-2] if len(data) > 1 else current
                change = ((current - prev) / prev) * 100
                
                index_data.append({
                    'Index': name,
                    'Value': f"{current:,.2f}",
                    'Change %': f"{change:+.2f}%"
                })
        except:
            pass
    
    if index_data:
        df = pd.DataFrame(index_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

elif st.session_state.page == "settings":
    st.title("⚙️ Settings")
    
    preferences = cache_manager.get_user_preferences()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Display Preferences")
        
        show_indicators = st.checkbox("Show Technical Indicators", value=preferences.get('show_technical_indicators', True))
        auto_refresh = st.checkbox("Auto Refresh Data", value=preferences.get('auto_refresh', False))
        
        default_period = st.selectbox(
            "Default Time Period",
            ["1mo", "3mo", "6mo", "1y", "2y"],
            index=3
        )
    
    with col2:
        st.subheader("Data Management")
        
        if st.button("Clear Search History"):
            cache_manager.clear_search_history()
            st.success("Search history cleared!")
        
        if st.button("Reset All Settings"):
            keys_to_remove = []
            for key in st.session_state.keys():
                if isinstance(key, str) and (key.startswith('user_preferences') or key.startswith('search_history')):
                    keys_to_remove.append(key)
            
            for key in keys_to_remove:
                del st.session_state[key]
            st.success("Settings reset!")
            st.rerun()
    
    if st.button("Save Settings", type="primary"):
        new_preferences = {
            'show_technical_indicators': show_indicators,
            'auto_refresh': auto_refresh,
            'default_period': default_period
        }
        cache_manager.save_user_preferences(new_preferences)
        st.success("Settings saved!")

render_footer()

st.markdown('</div>', unsafe_allow_html=True)
