import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

class MetricsCalculator:
    """Class to calculate various financial and technical metrics"""
    
    def __init__(self):
        pass
    
    def calculate_metrics(self, data: pd.DataFrame, info: Dict[Any, Any]) -> Dict[str, Any]:
        """
        Calculate key financial metrics for a stock
        
        Args:
            data: DataFrame with OHLCV data
            info: Dictionary with stock information from Yahoo Finance
            
        Returns:
            Dictionary with calculated metrics
        """
        if data.empty:
            return {}
        
        try:
            current_price = data['Close'].iloc[-1]
            previous_price = data['Close'].iloc[-2] if len(data) > 1 else current_price
            price_change = current_price - previous_price
            percent_change = (price_change / previous_price) * 100 if previous_price != 0 else 0
            
            # Calculate 52-week high and low
            high_52w = data['High'].max()
            low_52w = data['Low'].min()
            
            # Calculate average volume
            avg_volume = data['Volume'].mean()
            current_volume = data['Volume'].iloc[-1]
            
            # Format market cap
            market_cap = self._format_market_cap(info.get('marketCap', 0))
            
            metrics = {
                'Current Price': current_price,
                'Price Change': price_change,
                'Percent Change': percent_change,
                'Volume': int(current_volume),
                'Avg Volume': int(avg_volume),
                'Market Cap': market_cap,
                'P/E Ratio': info.get('trailingPE', 'N/A'),
                '52W High': high_52w,
                '52W Low': low_52w,
                'Beta': info.get('beta', 'N/A'),
                'Dividend Yield': self._format_percentage(info.get('dividendYield', 0))
            }
            
            return metrics
            
        except Exception as e:
            print(f"Error calculating metrics: {str(e)}")
            return {}
    
    def calculate_technical_indicators(self, data: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate technical indicators
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            Dictionary with technical indicators
        """
        if data.empty:
            return {}
        
        try:
            # Calculate Simple Moving Averages
            sma_20 = data['Close'].rolling(window=20).mean().iloc[-1]
            sma_50 = data['Close'].rolling(window=50).mean().iloc[-1]
            
            # Calculate RSI
            rsi = self._calculate_rsi(data['Close'])
            
            # Calculate Bollinger Bands
            bb_upper, bb_lower = self._calculate_bollinger_bands(data['Close'])
            
            # Calculate MACD
            macd_line, macd_signal = self._calculate_macd(data['Close'])
            
            indicators = {
                'sma_20': sma_20 if not np.isnan(sma_20) else 0,
                'sma_50': sma_50 if not np.isnan(sma_50) else 0,
                'rsi': rsi,
                'bb_upper': bb_upper,
                'bb_lower': bb_lower,
                'macd_line': macd_line,
                'macd_signal': macd_signal
            }
            
            return indicators
            
        except Exception as e:
            print(f"Error calculating technical indicators: {str(e)}")
            return {}
    
    def calculate_price_statistics(self, data: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate price statistics
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            Dictionary with price statistics
        """
        if data.empty:
            return {}
        
        try:
            stats = {
                'current_price': data['Close'].iloc[-1],
                'high_52w': data['High'].max(),
                'low_52w': data['Low'].min(),
                'avg_volume': data['Volume'].mean(),
                'price_volatility': data['Close'].pct_change().std() * np.sqrt(252) * 100,  # Annualized volatility
                'avg_price': data['Close'].mean(),
                'median_price': data['Close'].median()
            }
            
            return stats
            
        except Exception as e:
            print(f"Error calculating price statistics: {str(e)}")
            return {}
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> float:
        """Calculate Relative Strength Index"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi.iloc[-1] if not np.isnan(rsi.iloc[-1]) else 50.0
            
        except:
            return 50.0
    
    def _calculate_bollinger_bands(self, prices: pd.Series, period: int = 20, std_dev: int = 2) -> tuple:
        """Calculate Bollinger Bands"""
        try:
            sma = prices.rolling(window=period).mean()
            std = prices.rolling(window=period).std()
            
            upper_band = sma + (std * std_dev)
            lower_band = sma - (std * std_dev)
            
            return upper_band.iloc[-1], lower_band.iloc[-1]
            
        except:
            return 0.0, 0.0
    
    def _calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        try:
            ema_fast = prices.ewm(span=fast).mean()
            ema_slow = prices.ewm(span=slow).mean()
            
            macd_line = ema_fast - ema_slow
            macd_signal = macd_line.ewm(span=signal).mean()
            
            return macd_line.iloc[-1], macd_signal.iloc[-1]
            
        except:
            return 0.0, 0.0
    
    def _format_market_cap(self, market_cap: Optional[float]) -> str:
        """Format market cap with appropriate suffix"""
        if not market_cap or market_cap == 0:
            return "N/A"
        
        if market_cap >= 1e12:
            return f"${market_cap/1e12:.2f}T"
        elif market_cap >= 1e9:
            return f"${market_cap/1e9:.2f}B"
        elif market_cap >= 1e6:
            return f"${market_cap/1e6:.2f}M"
        else:
            return f"${market_cap:.0f}"
    
    def _format_percentage(self, value: Optional[float]) -> str:
        """Format percentage values"""
        if value is None or value == 0:
            return "N/A"
        return f"{value * 100:.2f}%"
    
    def calculate_portfolio_metrics(self, all_data: Dict[str, pd.DataFrame], weights: Dict[str, float] = None) -> Dict[str, float]:
        """
        Calculate portfolio-level metrics
        
        Args:
            all_data: Dictionary with symbol as key and DataFrame as value
            weights: Dictionary with symbol as key and weight as value
            
        Returns:
            Dictionary with portfolio metrics
        """
        if not all_data:
            return {}
        
        try:
            if weights is None:
                # Equal weights if not specified
                weights = {symbol: 1.0/len(all_data) for symbol in all_data.keys()}
            
            # Calculate portfolio returns
            portfolio_returns = 0
            portfolio_value = 0
            
            for symbol, data in all_data.items():
                if symbol in weights:
                    current_price = data['Close'].iloc[-1]
                    initial_price = data['Close'].iloc[0]
                    stock_return = (current_price - initial_price) / initial_price
                    
                    portfolio_returns += stock_return * weights[symbol]
                    portfolio_value += current_price * weights[symbol]
            
            metrics = {
                'portfolio_return': portfolio_returns * 100,
                'portfolio_value': portfolio_value,
                'num_stocks': len(all_data)
            }
            
            return metrics
            
        except Exception as e:
            print(f"Error calculating portfolio metrics: {str(e)}")
            return {}
