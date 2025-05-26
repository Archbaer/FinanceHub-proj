from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

class DataService:
    def __init__(self):
        self.cache = {}
    
    def get_stock_data(self, symbol, period="1y"):
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval="1d")
            
            if data.empty:
                return None
            
            data.reset_index(inplace=True)
            return data.to_dict('records')
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_stock_info(self, symbol):
        try:
            ticker = yf.Ticker(symbol)
            return ticker.info
        except:
            return {}
    
    def get_crypto_data(self, symbol, period="1y"):
        if not symbol.endswith('-USD'):
            symbol = f"{symbol}-USD"
        return self.get_stock_data(symbol, period)

data_service = DataService()

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/stock/<symbol>')
def get_stock(symbol):
    period = request.args.get('period', '1y')
    data = data_service.get_stock_data(symbol.upper(), period)
    
    if data is None:
        return jsonify({"error": "Stock not found"}), 404
    
    info = data_service.get_stock_info(symbol.upper())
    
    return jsonify({
        "symbol": symbol.upper(),
        "data": data,
        "info": info,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/crypto/<symbol>')
def get_crypto(symbol):
    period = request.args.get('period', '1y')
    data = data_service.get_crypto_data(symbol.upper(), period)
    
    if data is None:
        return jsonify({"error": "Crypto not found"}), 404
    
    return jsonify({
        "symbol": symbol.upper(),
        "data": data,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/trending/stocks')
def trending_stocks():
    symbols = ['AAPL', 'TSLA', 'NVDA', 'MSFT', 'GOOGL']
    trending_data = []
    
    for symbol in symbols:
        data = data_service.get_stock_data(symbol, "5d")
        if data and len(data) > 1:
            current = data[-1]['Close']
            prev = data[-2]['Close']
            change = ((current - prev) / prev) * 100
            
            trending_data.append({
                'symbol': symbol,
                'price': current,
                'change': change
            })
    
    return jsonify(trending_data)

@app.route('/api/trending/crypto')
def trending_crypto():
    symbols = ['BTC-USD', 'ETH-USD', 'SOL-USD']
    crypto_data = []
    
    for symbol in symbols:
        data = data_service.get_crypto_data(symbol, "5d")
        if data and len(data) > 1:
            current = data[-1]['Close']
            prev = data[-2]['Close']
            change = ((current - prev) / prev) * 100
            
            crypto_data.append({
                'symbol': symbol.replace('-USD', ''),
                'price': current,
                'change': change
            })
    
    return jsonify(crypto_data)

@app.route('/api/portfolio/calculate', methods=['POST'])
def calculate_portfolio():
    portfolio_data = request.json
    holdings = portfolio_data.get('holdings', {})
    
    total_investment = 0
    current_value = 0
    
    for symbol, holding in holdings.items():
        shares = holding['shares']
        purchase_price = holding['purchase_price']
        
        data = data_service.get_stock_data(symbol, "1mo")
        if data:
            current_price = data[-1]['Close']
            investment = shares * purchase_price
            value = shares * current_price
            
            total_investment += investment
            current_value += value
    
    total_return = current_value - total_investment
    return_pct = (total_return / total_investment * 100) if total_investment > 0 else 0
    
    return jsonify({
        'total_investment': total_investment,
        'current_value': current_value,
        'total_return': total_return,
        'return_pct': return_pct
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(port=port, debug=False)