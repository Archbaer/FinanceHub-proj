import pandas as pd
import io
from datetime import datetime
from utils.data_fetcher import StockDataFetcher

class DataExporter:
    def __init__(self):
        self.data_fetcher = StockDataFetcher()
    
    def export_stock_historical_data(self, symbol: str, period: str = "1y") -> str:
        """
        Export complete historical daily data for a stock as CSV
        
        Args:
            symbol: Stock symbol
            period: Time period for data export
            
        Returns:
            CSV string with complete daily data
        """
        try:
            data = self.data_fetcher.get_stock_data(symbol, period)
            info = self.data_fetcher.get_stock_info(symbol)
            
            if data is None or data.empty:
                return ""
            
            # Create comprehensive dataset
            export_data = data.copy()
            
            # Add calculated fields
            export_data['Daily_Change'] = export_data['Close'] - export_data['Open']
            export_data['Daily_Change_Pct'] = ((export_data['Close'] - export_data['Open']) / export_data['Open']) * 100
            export_data['Price_Range'] = export_data['High'] - export_data['Low']
            export_data['Price_Range_Pct'] = ((export_data['High'] - export_data['Low']) / export_data['Low']) * 100
            
            # Add moving averages
            export_data['MA_7'] = export_data['Close'].rolling(window=7).mean()
            export_data['MA_20'] = export_data['Close'].rolling(window=20).mean()
            export_data['MA_50'] = export_data['Close'].rolling(window=50).mean()
            
            # Add volatility
            export_data['Volatility_7d'] = export_data['Close'].pct_change().rolling(window=7).std()
            export_data['Volatility_20d'] = export_data['Close'].pct_change().rolling(window=20).std()
            
            # Add volume analysis
            export_data['Volume_MA_20'] = export_data['Volume'].rolling(window=20).mean()
            export_data['Volume_Ratio'] = export_data['Volume'] / export_data['Volume_MA_20']
            
            # Add company info as first row metadata
            metadata = {
                'Date': 'METADATA',
                'Open': f"Company: {info.get('longName', 'N/A')}",
                'High': f"Sector: {info.get('sector', 'N/A')}",
                'Low': f"Industry: {info.get('industry', 'N/A')}",
                'Close': f"Market Cap: {info.get('marketCap', 'N/A')}",
                'Volume': f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                'Dividends': f"Symbol: {symbol}",
                'Stock Splits': f"Period: {period}",
                'Daily_Change': 'START_OF_DATA',
                'Daily_Change_Pct': '',
                'Price_Range': '',
                'Price_Range_Pct': '',
                'MA_7': '',
                'MA_20': '',
                'MA_50': '',
                'Volatility_7d': '',
                'Volatility_20d': '',
                'Volume_MA_20': '',
                'Volume_Ratio': ''
            }
            
            # Insert metadata row
            metadata_df = pd.DataFrame([metadata])
            final_data = pd.concat([metadata_df, export_data], ignore_index=True)
            
            # Convert to CSV
            csv_buffer = io.StringIO()
            final_data.to_csv(csv_buffer, index=False, float_format='%.6f')
            return csv_buffer.getvalue()
            
        except Exception as e:
            print(f"Export error: {e}")
            return ""
    
    def export_multiple_stocks_comparison(self, symbols: list, period: str = "1y") -> str:
        """
        Export comparison data for multiple stocks
        
        Args:
            symbols: List of stock symbols
            period: Time period for data export
            
        Returns:
            CSV string with comparison data
        """
        try:
            all_data = []
            
            for symbol in symbols:
                data = self.data_fetcher.get_stock_data(symbol, period)
                if data is not None and not data.empty:
                    # Add symbol column
                    data['Symbol'] = symbol
                    data['Daily_Return'] = data['Close'].pct_change() * 100
                    all_data.append(data)
            
            if not all_data:
                return ""
            
            # Combine all data
            combined_data = pd.concat(all_data, ignore_index=True)
            
            # Sort by date and symbol
            combined_data = combined_data.sort_values(['Date', 'Symbol'])
            
            csv_buffer = io.StringIO()
            combined_data.to_csv(csv_buffer, index=False, float_format='%.6f')
            return csv_buffer.getvalue()
            
        except Exception as e:
            print(f"Export error: {e}")
            return ""
    
    def export_crypto_data(self, symbol: str, period: str = "1y") -> str:
        """
        Export cryptocurrency historical data
        
        Args:
            symbol: Crypto symbol (e.g., BTC-USD)
            period: Time period for data export
            
        Returns:
            CSV string with crypto data
        """
        try:
            from utils.crypto_fetcher import CryptoDataFetcher
            crypto_fetcher = CryptoDataFetcher()
            
            data = crypto_fetcher.get_crypto_data(symbol, period)
            if data is None or data.empty:
                return ""
            
            # Add crypto-specific calculations
            data['Daily_Return'] = data['Close'].pct_change() * 100
            data['Cumulative_Return'] = (1 + data['Close'].pct_change()).cumprod() - 1
            data['Rolling_Volatility'] = data['Close'].pct_change().rolling(window=30).std() * (365**0.5) * 100
            
            csv_buffer = io.StringIO()
            data.to_csv(csv_buffer, index=False, float_format='%.8f')
            return csv_buffer.getvalue()
            
        except Exception as e:
            print(f"Crypto export error: {e}")
            return ""