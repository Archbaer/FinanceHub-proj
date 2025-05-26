import yfinance as yf
import pandas as pd
import streamlit as st
from typing import Optional, Dict, Any, List

class CryptoDataFetcher:
    def __init__(self):
        self.crypto_symbols = {
            'BTC-USD': 'Bitcoin',
            'ETH-USD': 'Ethereum',
            'BNB-USD': 'Binance Coin',
            'XRP-USD': 'Ripple',
            'ADA-USD': 'Cardano',
            'SOL-USD': 'Solana',
            'DOGE-USD': 'Dogecoin',
            'DOT-USD': 'Polkadot',
            'MATIC-USD': 'Polygon',
            'SHIB-USD': 'Shiba Inu'
        }
    
    @st.cache_data(ttl=300)
    def get_crypto_data(_self, symbol: str, period: str = "1y") -> Optional[pd.DataFrame]:
        try:
            if not symbol.endswith('-USD'):
                symbol = f"{symbol}-USD"
            
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval="1d")
            
            if data.empty:
                return None
            
            data.reset_index(inplace=True)
            return data
            
        except Exception as e:
            st.error(f"Error fetching crypto data for {symbol}: {str(e)}")
            return None
    
    @st.cache_data(ttl=3600)
    def get_crypto_info(_self, symbol: str) -> Dict[Any, Any]:
        try:
            if not symbol.endswith('-USD'):
                symbol = f"{symbol}-USD"
                
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return info
            
        except Exception as e:
            return {}
    
    def get_popular_cryptos(self) -> Dict[str, str]:
        return self.crypto_symbols
    
    def get_trending_cryptos(self) -> List[str]:
        return ['BTC-USD', 'ETH-USD', 'SOL-USD', 'DOGE-USD', 'ADA-USD']