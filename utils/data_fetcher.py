import yfinance as yf
import pandas as pd
import streamlit as st
from typing import Optional, Dict, Any

class StockDataFetcher:
    """Class to handle stock data fetching from Yahoo Finance"""
    
    def __init__(self):
        self.cache = {}
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_stock_data(_self, symbol: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """
        Fetch stock price data from Yahoo Finance
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            
        Returns:
            DataFrame with stock price data or None if error
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval="1d")
            
            if data.empty:
                st.error(f"No data found for symbol: {symbol}")
                return None
            
            # Reset index to make Date a column
            data.reset_index(inplace=True)
            
            return data
            
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def get_stock_info(_self, symbol: str) -> Dict[Any, Any]:
        """
        Fetch stock information from Yahoo Finance
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            Dictionary with stock information
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return info
            
        except Exception as e:
            st.error(f"Error fetching info for {symbol}: {str(e)}")
            return {}
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_multiple_stocks_data(_self, symbols: list, period: str = "1y") -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple stocks
        
        Args:
            symbols: List of stock symbols
            period: Time period
            
        Returns:
            Dictionary with symbol as key and DataFrame as value
        """
        results = {}
        
        for symbol in symbols:
            data = _self.get_stock_data(symbol, period)
            if data is not None:
                results[symbol] = data
        
        return results
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """
        Get current stock price
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Current price or None if error
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="1m")
            
            if not data.empty:
                return data['Close'].iloc[-1]
            
            return None
            
        except Exception as e:
            st.error(f"Error fetching current price for {symbol}: {str(e)}")
            return None
    
    def validate_symbol(self, symbol: str) -> bool:
        """
        Validate if a stock symbol exists
        
        Args:
            symbol: Stock symbol to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Check if we got valid info
            return 'regularMarketPrice' in info or 'currentPrice' in info
            
        except:
            return False
