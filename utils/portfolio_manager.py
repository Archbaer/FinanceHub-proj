import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json

class PortfolioManager:
    """Class to manage portfolio tracking and performance analytics"""
    
    def __init__(self):
        self.portfolio_key = "user_portfolios"
        
    def save_portfolio(self, name: str, holdings: Dict[str, Dict]) -> bool:
        """
        Save portfolio to session state
        
        Args:
            name: Portfolio name
            holdings: Dictionary with symbol as key and holding details as value
            
        Returns:
            True if saved successfully
        """
        try:
            if self.portfolio_key not in st.session_state:
                st.session_state[self.portfolio_key] = {}
            
            portfolio_data = {
                'holdings': holdings,
                'created_date': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            }
            
            st.session_state[self.portfolio_key][name] = portfolio_data
            return True
            
        except Exception as e:
            st.error(f"Error saving portfolio: {str(e)}")
            return False
    
    def load_portfolio(self, name: str) -> Optional[Dict]:
        """
        Load portfolio from session state
        
        Args:
            name: Portfolio name
            
        Returns:
            Portfolio data or None if not found
        """
        try:
            if self.portfolio_key in st.session_state:
                return st.session_state[self.portfolio_key].get(name)
            return None
            
        except Exception as e:
            st.error(f"Error loading portfolio: {str(e)}")
            return None
    
    def get_all_portfolios(self) -> Dict[str, Dict]:
        """
        Get all saved portfolios
        
        Returns:
            Dictionary of all portfolios
        """
        if self.portfolio_key in st.session_state:
            return st.session_state[self.portfolio_key]
        return {}
    
    def delete_portfolio(self, name: str) -> bool:
        """
        Delete a portfolio
        
        Args:
            name: Portfolio name
            
        Returns:
            True if deleted successfully
        """
        try:
            if self.portfolio_key in st.session_state and name in st.session_state[self.portfolio_key]:
                del st.session_state[self.portfolio_key][name]
                return True
            return False
            
        except Exception as e:
            st.error(f"Error deleting portfolio: {str(e)}")
            return False
    
    def calculate_portfolio_performance(self, holdings: Dict[str, Dict], all_data: Dict[str, pd.DataFrame]) -> Dict[str, float]:
        """
        Calculate comprehensive portfolio performance metrics
        
        Args:
            holdings: Dictionary with symbol and holding details
            all_data: Dictionary with symbol as key and price data as value
            
        Returns:
            Dictionary with performance metrics
        """
        try:
            total_investment = 0
            current_value = 0
            total_shares = 0
            weighted_returns = 0
            
            for symbol, holding in holdings.items():
                if symbol in all_data:
                    shares = holding['shares']
                    purchase_price = holding['purchase_price']
                    current_price = all_data[symbol]['Close'].iloc[-1]
                    
                    investment = shares * purchase_price
                    value = shares * current_price
                    
                    total_investment += investment
                    current_value += value
                    total_shares += shares
                    
                    # Calculate individual stock return
                    stock_return = (current_price - purchase_price) / purchase_price
                    weight = investment / sum(h['shares'] * h['purchase_price'] for h in holdings.values())
                    weighted_returns += stock_return * weight
            
            # Calculate portfolio metrics
            total_return = current_value - total_investment
            total_return_pct = (total_return / total_investment * 100) if total_investment > 0 else 0
            
            # Calculate volatility (using 30-day period)
            portfolio_volatility = self._calculate_portfolio_volatility(holdings, all_data)
            
            # Calculate Sharpe ratio (assuming 2% risk-free rate)
            risk_free_rate = 0.02
            sharpe_ratio = (weighted_returns - risk_free_rate) / portfolio_volatility if portfolio_volatility > 0 else 0
            
            # Calculate maximum drawdown
            max_drawdown = self._calculate_max_drawdown(holdings, all_data)
            
            metrics = {
                'total_investment': total_investment,
                'current_value': current_value,
                'total_return': total_return,
                'total_return_pct': total_return_pct,
                'weighted_return_pct': weighted_returns * 100,
                'portfolio_volatility': portfolio_volatility * 100,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown * 100,
                'number_of_stocks': len(holdings)
            }
            
            return metrics
            
        except Exception as e:
            st.error(f"Error calculating portfolio performance: {str(e)}")
            return {}
    
    def _calculate_portfolio_volatility(self, holdings: Dict[str, Dict], all_data: Dict[str, pd.DataFrame], days: int = 30) -> float:
        """Calculate portfolio volatility based on recent price movements"""
        try:
            if not holdings or not all_data:
                return 0.0
            
            # Get recent returns for each stock
            portfolio_returns = []
            total_investment = sum(h['shares'] * h['purchase_price'] for h in holdings.values())
            
            # Calculate daily portfolio returns for the last 30 days
            for i in range(min(days, len(next(iter(all_data.values()))) - 1)):
                daily_return = 0
                for symbol, holding in holdings.items():
                    if symbol in all_data and len(all_data[symbol]) > i + 1:
                        weight = (holding['shares'] * holding['purchase_price']) / total_investment
                        price_today = all_data[symbol]['Close'].iloc[-(i+1)]
                        price_yesterday = all_data[symbol]['Close'].iloc[-(i+2)]
                        stock_return = (price_today - price_yesterday) / price_yesterday
                        daily_return += weight * stock_return
                
                portfolio_returns.append(daily_return)
            
            return np.std(portfolio_returns) * np.sqrt(252) if portfolio_returns else 0.0
            
        except:
            return 0.0
    
    def _calculate_max_drawdown(self, holdings: Dict[str, Dict], all_data: Dict[str, pd.DataFrame]) -> float:
        """Calculate maximum drawdown of the portfolio"""
        try:
            if not holdings or not all_data:
                return 0.0
            
            # Calculate portfolio value over time
            min_length = min(len(data) for data in all_data.values())
            portfolio_values = []
            
            for i in range(min_length):
                daily_value = 0
                for symbol, holding in holdings.items():
                    if symbol in all_data:
                        price = all_data[symbol]['Close'].iloc[i]
                        daily_value += holding['shares'] * price
                portfolio_values.append(daily_value)
            
            # Calculate drawdowns
            portfolio_values = np.array(portfolio_values)
            peaks = np.maximum.accumulate(portfolio_values)
            drawdowns = (portfolio_values - peaks) / peaks
            
            return abs(np.min(drawdowns)) if len(drawdowns) > 0 else 0.0
            
        except:
            return 0.0
    
    def generate_portfolio_allocation_chart(self, holdings: Dict[str, Dict], all_data: Dict[str, pd.DataFrame]):
        """Generate portfolio allocation pie chart"""
        import plotly.graph_objects as go
        
        try:
            labels = []
            values = []
            colors = []
            
            color_palette = ['#0052CC', '#00875A', '#DE350B', '#8777D9', '#FFC400', 
                           '#6554C0', '#00B8D9', '#36B37E', '#FF8B00', '#FF5630']
            
            for i, (symbol, holding) in enumerate(holdings.items()):
                if symbol in all_data:
                    current_price = all_data[symbol]['Close'].iloc[-1]
                    value = holding['shares'] * current_price
                    
                    labels.append(f"{symbol}")
                    values.append(value)
                    colors.append(color_palette[i % len(color_palette)])
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                marker_colors=colors,
                textinfo='label+percent',
                textposition='outside',
                hovertemplate='<b>%{label}</b><br>Value: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>'
            )])
            
            fig.update_layout(
                title='Portfolio Allocation',
                template='plotly_white',
                height=400,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05
                )
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error generating allocation chart: {str(e)}")
            return None
    
    def generate_performance_timeline_chart(self, holdings: Dict[str, Dict], all_data: Dict[str, pd.DataFrame]):
        """Generate portfolio performance over time chart"""
        import plotly.graph_objects as go
        
        try:
            # Calculate portfolio value over time
            min_length = min(len(data) for data in all_data.values())
            dates = []
            portfolio_values = []
            initial_investment = sum(h['shares'] * h['purchase_price'] for h in holdings.values())
            
            for i in range(min_length):
                daily_value = 0
                date = None
                for symbol, holding in holdings.items():
                    if symbol in all_data:
                        price = all_data[symbol]['Close'].iloc[i]
                        daily_value += holding['shares'] * price
                        if date is None:
                            date = all_data[symbol]['Date'].iloc[i]
                
                dates.append(date)
                portfolio_values.append(daily_value)
            
            # Calculate percentage returns
            portfolio_returns = [(val / initial_investment - 1) * 100 for val in portfolio_values]
            
            fig = go.Figure()
            
            # Add portfolio performance line
            fig.add_trace(go.Scatter(
                x=dates,
                y=portfolio_returns,
                mode='lines',
                name='Portfolio Performance',
                line=dict(color='#0052CC', width=3),
                hovertemplate='Date: %{x}<br>Return: %{y:.2f}%<extra></extra>'
            ))
            
            # Add benchmark line (0% return)
            fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5, 
                         annotation_text="Break-even")
            
            fig.update_layout(
                title='Portfolio Performance Over Time',
                xaxis_title='Date',
                yaxis_title='Return (%)',
                template='plotly_white',
                height=400,
                hovermode='x unified'
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error generating performance chart: {str(e)}")
            return None