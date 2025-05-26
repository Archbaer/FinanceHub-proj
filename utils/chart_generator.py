import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict

class ChartGenerator:
    """Class to generate interactive charts for stock analysis"""
    
    def __init__(self):
        # Color scheme for charts
        self.colors = {
            'primary': '#0052CC',
            'secondary': '#00875A',
            'warning': '#DE350B',
            'background': '#F4F5F7',
            'text': '#172B4D',
            'positive': '#00875A',
            'negative': '#DE350B'
        }
    
    def create_candlestick_chart(self, data: pd.DataFrame, symbol: str) -> go.Figure:
        """
        Create a candlestick chart with volume
        
        Args:
            data: DataFrame with OHLCV data
            symbol: Stock symbol for title
            
        Returns:
            Plotly figure object
        """
        # Create subplot with secondary y-axis
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=(f'{symbol} - Price', 'Volume'),
            row_width=[0.2, 0.7]
        )
        
        # Add candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Price',
                increasing_line_color=self.colors['positive'],
                decreasing_line_color=self.colors['negative']
            ),
            row=1, col=1
        )
        
        # Add volume bars
        colors = np.where(data['Close'] >= data['Open'], 
                         self.colors['positive'], 
                         self.colors['negative'])
        
        fig.add_trace(
            go.Bar(
                x=data['Date'],
                y=data['Volume'],
                name='Volume',
                marker_color=colors,
                opacity=0.7
            ),
            row=2, col=1
        )
        
        # Update layout
        fig.update_layout(
            title=f'{symbol} - Stock Price and Volume Analysis',
            xaxis_rangeslider_visible=False,
            height=600,
            showlegend=False,
            template='plotly_white'
        )
        
        # Update axes
        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        fig.update_xaxes(title_text="Date", row=2, col=1)
        
        return fig
    
    def create_line_chart(self, data: pd.DataFrame, symbol: str) -> go.Figure:
        """
        Create a simple line chart for stock price
        
        Args:
            data: DataFrame with price data
            symbol: Stock symbol for title
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(
                x=data['Date'],
                y=data['Close'],
                mode='lines',
                name=f'{symbol} Close Price',
                line=dict(color=self.colors['primary'], width=2)
            )
        )
        
        fig.update_layout(
            title=f'{symbol} - Stock Price Trend',
            xaxis_title='Date',
            yaxis_title='Price ($)',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def create_volume_chart(self, data: pd.DataFrame, symbol: str) -> go.Figure:
        """
        Create a volume chart
        
        Args:
            data: DataFrame with volume data
            symbol: Stock symbol for title
            
        Returns:
            Plotly figure object
        """
        # Color volume bars based on price movement
        colors = np.where(data['Close'] >= data['Open'], 
                         self.colors['positive'], 
                         self.colors['negative'])
        
        fig = go.Figure()
        
        fig.add_trace(
            go.Bar(
                x=data['Date'],
                y=data['Volume'],
                name='Volume',
                marker_color=colors,
                opacity=0.7
            )
        )
        
        fig.update_layout(
            title=f'{symbol} - Trading Volume',
            xaxis_title='Date',
            yaxis_title='Volume',
            template='plotly_white',
            height=300
        )
        
        return fig
    
    def create_comparison_chart(self, all_data: Dict[str, pd.DataFrame]) -> go.Figure:
        """
        Create a comparison chart for multiple stocks
        
        Args:
            all_data: Dictionary with symbol as key and DataFrame as value
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        colors = px.colors.qualitative.Set1
        
        for i, (symbol, data) in enumerate(all_data.items()):
            # Normalize prices to percentage change from first day
            normalized_prices = (data['Close'] / data['Close'].iloc[0] - 1) * 100
            
            fig.add_trace(
                go.Scatter(
                    x=data['Date'],
                    y=normalized_prices,
                    mode='lines',
                    name=symbol,
                    line=dict(color=colors[i % len(colors)], width=2)
                )
            )
        
        fig.update_layout(
            title='Stock Price Comparison (Normalized %)',
            xaxis_title='Date',
            yaxis_title='Price Change (%)',
            template='plotly_white',
            height=500,
            hovermode='x unified'
        )
        
        # Add horizontal line at 0%
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        return fig
    
    def create_simple_line_chart(self, data: pd.DataFrame, symbol: str) -> go.Figure:
        """
        Create a simple line chart for individual stock in comparison view
        
        Args:
            data: DataFrame with price data
            symbol: Stock symbol for title
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        # Calculate price change
        price_change = data['Close'].iloc[-1] - data['Close'].iloc[0]
        color = self.colors['positive'] if price_change >= 0 else self.colors['negative']
        
        fig.add_trace(
            go.Scatter(
                x=data['Date'],
                y=data['Close'],
                mode='lines',
                name=symbol,
                line=dict(color=color, width=2),
                fill='tonexty' if price_change >= 0 else None,
                fillcolor=f'rgba({self._hex_to_rgb(color)}, 0.1)'
            )
        )
        
        fig.update_layout(
            title=f'{symbol}',
            xaxis_title='Date',
            yaxis_title='Price ($)',
            template='plotly_white',
            height=300,
            showlegend=False
        )
        
        return fig
    
    def create_performance_chart(self, metrics_df: pd.DataFrame) -> go.Figure:
        """
        Create a performance comparison chart
        
        Args:
            metrics_df: DataFrame with calculated metrics
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        # Create bar chart for percent change
        colors = [self.colors['positive'] if x >= 0 else self.colors['negative'] 
                 for x in metrics_df['Percent Change']]
        
        fig.add_trace(
            go.Bar(
                x=metrics_df['Symbol'],
                y=metrics_df['Percent Change'],
                marker_color=colors,
                name='Percent Change',
                text=[f'{x:.2f}%' for x in metrics_df['Percent Change']],
                textposition='outside'
            )
        )
        
        fig.update_layout(
            title='Stock Performance Comparison',
            xaxis_title='Stock Symbol',
            yaxis_title='Percent Change (%)',
            template='plotly_white',
            height=400
        )
        
        # Add horizontal line at 0%
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        return fig
    
    def _hex_to_rgb(self, hex_color: str) -> str:
        """Convert hex color to RGB string"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f'{rgb[0]}, {rgb[1]}, {rgb[2]}'
