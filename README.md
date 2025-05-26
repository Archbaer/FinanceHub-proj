# FinanceHub - Professional Trading Dashboard

A comprehensive stock and cryptocurrency analysis platform with portfolio tracking and performance analytics.

## Features

### Core Functionality

- **Stock Analysis** - Real-time data from Yahoo Finance with interactive charts
- **Cryptocurrency Support** - Track Bitcoin, Ethereum, and other major cryptos
- **Portfolio Management** - Create, track, and analyze investment portfolios
- **Memory Cache** - Remembers last 10 searched stocks in browser session
- **Dark/Light Mode** - Toggle between themes for comfortable viewing

### Advanced Analytics

- **Technical Indicators** - RSI, Moving Averages, Bollinger Bands, MACD
- **Performance Metrics** - Sharpe ratio, volatility, maximum drawdown
- **Interactive Charts** - Candlestick, volume, and comparison visualizations
- **Real-time Data** - Live market data with automatic updates

### User Experience

- **Multi-page Navigation** - Home, Stocks, Crypto, Portfolio, Market Overview
- **Quick Search** - Sidebar search with recent history
- **Trending Tickers** - Popular stocks and crypto on homepage
- **CSV Export** - Download portfolio reports and stock data

## Architecture

### Monolithic Version (Current)

- **Frontend**: Streamlit web application
- **Data**: Yahoo Finance API integration
- **Storage**: Session-based caching

### Microservices Version (Ready for Production)

- **Backend**: Flask API service (Port 8000)
- **Frontend**: Streamlit UI service (Port 8501)
- **Proxy**: Nginx load balancer (Port 80)
- **Container**: Docker & Docker Compose ready
- **Orchestration**: Kubernetes manifests for cloud deployment

## Quick Start

```
docker-compose up

# Acess at localhost:5000
```

## Project Structure

```
FinanceHub/
├── app.py                              # Main Streamlit application
├── app_new.py                          # Enhanced version with all features
├── components/                         # UI components
│   ├── home_screen.py                 # Landing page with trending data
│   ├── footer.py                      # Footer with social links
│   └── theme_manager.py               # Dark/light mode toggle
├── utils/                             # Core business logic
│   ├── data_fetcher.py               # Stock data from Yahoo Finance
│   ├── crypto_fetcher.py             # Cryptocurrency data
│   ├── chart_generator.py            # Interactive chart creation
│   ├── metrics_calculator.py         # Financial calculations
│   ├── portfolio_manager.py          # Portfolio tracking
│   └── cache_manager.py              # Search history & preferences
├── backend/                           # Microservice API
│   ├── app.py                        # Flask REST API
│   ├── requirements.txt              # Python dependencies
│   └── Dockerfile                    # Container build
├── frontend/                          # Microservice UI
│   ├── app.py                        # Streamlit frontend
│   ├── requirements.txt              # UI dependencies
│   └── Dockerfile                    # Container build
├── k8s/                              # Kubernetes deployment
│   ├── backend-deployment.yaml       # API service config
│   ├── frontend-deployment.yaml      # UI service config
│   └── ingress.yaml                  # Load balancer config
├── docker-compose.yml                # Single container setup
├── docker-compose-microservices.yml  # Multi-service setup
├── nginx.conf                        # Reverse proxy config
└── .streamlit/config.toml            # Theme configuration
```

## Features Implemented

✅ **Memory cache for last 10 stock searches**
✅ **Home screen with trending stocks/crypto**
✅ **Cryptocurrency analysis support**
✅ **Dark/Light mode toggle**
✅ **Multi-category navigation (Stocks, Crypto, Portfolio, Market)**
✅ **Footer with GitHub**
✅ **Microservices architecture (Frontend + Backend)**
✅ **Complete Docker setup with health checks**
✅ **Kubernetes deployment files for cloud**
✅ **Production-ready code structure**

## Social Links

- **GitHub**: https://github.com/archbaer

## Technology Stack

- **Frontend**: Streamlit, Plotly, Pandas
- **Backend**: Flask, Yahoo Finance API
- **Data**: Yahoo Finance (yfinance)
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Kubernetes
- **Proxy**: Nginx
- **Charts**: Plotly.js with custom styling

## Deployment Options

1. **Docker** - Single or multi-container setup
2. **AWS EKS** - Kubernetes cluster deployment
3. **Google GKE** - Google Cloud deployment
4. **Azure AKS** - Microsoft Azure deployment
