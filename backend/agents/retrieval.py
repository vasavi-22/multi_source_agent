import requests
import yfinance as yf
from bs4 import BeautifulSoup
from datetime import datetime
from rag.retriever import retrieve_context

def scrape_products(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        products = []

        for product in soup.find_all("article", class_="product_pod"):
            title = product.h3.a['title']
            price = product.find("p", class_="price_color").text
            products.append({
                "title": title,
                "price": price,
                "url": url,
                "timestamp": datetime.now().isoformat()
            })
        print(f"[INFO] Scraped {products} products from {url}")
        return products
    except requests.RequestException as e:
        print(f"[ERROR] Product scraping failed: {e}")
        return []

url = "http://books.toscrape.com/"
# result = scrape_products(url)
# for item in result:
#     print(item)

# FINANCE RETRIEVAL
def fetch_stock_data(symbol: str, period="5d", interval="1d"):
    """
    Fetch stock data using yfinance
    """
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period, interval=interval)
        if hist.empty:
            return []
        data = []
        for index, row in hist.iterrows():
            data.append({
                "symbol": symbol,
                "date": index.isoformat(),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"]),
            })
        print(f"[INFO] Retrieved {data} stock data points for {symbol}")
        return data
    except Exception as e:
        print(f"[ERROR] Stock data retrieval failed: {e}")
        return []

def fetch_forex_rate(pair="USDINR=X", period="5d"):
    """
    Fetch forex data using yfinance
    """
    try:
        forex = yf.Ticker(pair)
        hist = forex.history(period=period)
        if hist.empty:
            return []
        data = []
        for index, row in hist.iterrows():
            data.append({
                "pair": pair,
            "date": index.isoformat(),
            "rate": float(row["Close"]),
        })
        print(f"[INFO] Retrieved {data} forex data points for {pair}")
        return data
    except Exception as e:
        print(f"[ERROR] Forex data retrieval failed: {e}")
        return []
    
def knowledge_retrieval(state):

    # query = state.get("user_query")
    query = state.get("user_query") or "Provide market analysis"
    domain = state.get("data_type")  # "stock", "forex", "product"

    context = retrieve_context(query, domain)

    state["rag_context"] = context

    return state