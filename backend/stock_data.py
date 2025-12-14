"""
Stock data module with fallback mock data
This provides stock price information for financial queries
"""

# Realistic mock data for Indian stocks
STOCK_PRICES = {
    'ADANIGREEN.NS': {'price': 2045.50, 'name': 'Adani Green Energy'},
    'TATAMOTORS.NS': {'price': 1250.75, 'name': 'Tata Motors'},
    'INFY.NS': {'price': 2890.00, 'name': 'Infosys'},
    'TCS.NS': {'price': 3950.50, 'name': 'Tata Consultancy Services'},
    'RELIANCE.NS': {'price': 1320.00, 'name': 'Reliance Industries'},
    'HDFC.NS': {'price': 2650.00, 'name': 'HDFC Bank'},
    'ICICIBANK.NS': {'price': 990.50, 'name': 'ICICI Bank'},
    'SBIN.NS': {'price': 865.25, 'name': 'State Bank of India'},
}

def get_stock_price(symbol):
    """Get stock price for a given symbol"""
    if symbol in STOCK_PRICES:
        price = STOCK_PRICES[symbol]['price']
        return f"₹{price:.2f}"
    return None

def get_stock_week_return(symbol):
    """Get approximate last week's return"""
    # Return approximate returns for demo
    returns = {
        'ADANIGREEN.NS': '↑ 2.50%',
        'TATAMOTORS.NS': '↓ 1.20%',
        'INFY.NS': '↑ 3.10%',
        'TCS.NS': '↑ 0.85%',
        'RELIANCE.NS': '↓ 0.45%',
    }
    return returns.get(symbol, '~0%')

def get_stock_info(symbol):
    """Get stock info"""
    if symbol in STOCK_PRICES:
        info = STOCK_PRICES[symbol]
        return {
            'symbol': symbol,
            'name': info['name'],
            'price': f"₹{info['price']:.2f}",
        }
    return None

# NSE symbols mapping for Indian stocks
NSE_STOCKS = {
    'adanigreen': 'ADANIGREEN.NS',
    'adani green': 'ADANIGREEN.NS',
    'adani': 'ADANIGREEN.NS',
    'tata motors': 'TATAMOTORS.NS',
    'tatamotors': 'TATAMOTORS.NS',
    'tata': 'TATAMOTORS.NS',
    'infosys': 'INFY.NS',
    'infy': 'INFY.NS',
    'tcs': 'TCS.NS',
    'tata consultancy': 'TCS.NS',
    'hdfc': 'HDFC.NS',
    'hdfc bank': 'HDFC.NS',
    'icici': 'ICICIBANK.NS',
    'icici bank': 'ICICIBANK.NS',
    'sbi': 'SBIN.NS',
    'state bank': 'SBIN.NS',
    'reliance': 'RELIANCE.NS',
}

def resolve_stock_symbol(query):
    """Resolve stock name to NSE symbol"""
    query_lower = query.lower().strip()
    query_upper = query.upper().strip()
    
    # Check dictionary for matches
    for key, symbol in NSE_STOCKS.items():
        if key in query_lower:
            return symbol
    
    # If already in NSE format
    if query_upper.endswith('.NS') or query_upper.endswith('.BO'):
        return query_upper
    
    # Default format
    return f"{query.upper()}.NS"
