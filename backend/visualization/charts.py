import matplotlib.pyplot as plt

def plot_prices(products, top_n=5, sort_by_price=True):
    """
    Plots product prices from structured LangGraph output.

    :param products: List of structured product nodes
    :param top_n: Number of products to display
    :param sort_by_price: Whether to sort by ascending price
    """

    if not products:
        print("No products available for visualization.")
        return
    # Extract product_node safely
    product_nodes = [
        p.get("product_node", {})
        for p in products
        if p.get("product_node")
    ]
    if not product_nodes:
        print("No valid product nodes found.")
        return

    # Remove products without valid price
    product_nodes = [
        p for p in product_nodes
        if isinstance(p.get("price"), (int, float))
    ]

    if not product_nodes:
        print("No products with valid prices found.")
        return

    # Sort if needed
    if sort_by_price:
        product_nodes = sorted(product_nodes, key=lambda x: x["price"])

    # Limit results
    product_nodes = product_nodes[:top_n]

    names = [p.get("name", "Unknown") for p in product_nodes]
    prices = [p.get("price", 0) for p in product_nodes]

    # Plot
    plt.figure(figsize=(10, 5))
    plt.bar(names, prices)
    plt.xticks(rotation=45, ha="right")
    plt.title("Product Price Comparison")
    plt.xlabel("Product")
    plt.ylabel("Price")
    plt.tight_layout()
    plt.show()

def plot_stock_trend(structured_stocks):
    stock_nodes = [s["stock_node"] for s in structured_stocks]

    dates = [s["date"] for s in stock_nodes]
    closes = [s["close"] for s in stock_nodes]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, closes)
    plt.xticks(rotation=45)
    plt.title("Stock Closing Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.tight_layout()
    plt.show()