def check_price_threshold(structured_products, threshold: float):
    alerts = []
    for product in structured_products:
        node = product.get("product_node", {})
        price = node.get("price")
        if isinstance(price, (int, float)) and price < threshold:
            alerts.append(node)
    return alerts

def check_stock_threshold(structured_stock_data, threshold: float):
    alerts = []
    for stock in structured_stock_data:
        node = stock.get("stock_node", {})
        close_price = node.get("close")

        if isinstance(close_price, (int, float)) and close_price > threshold:
            alerts.append(node)
    return alerts


def check_forex_threshold(structured_forex_data, threshold: float):
    alerts = []
    for forex in structured_forex_data:
        node = forex.get("forex_node", {})
        rate = node.get("rate")

        if isinstance(rate, (int, float)) and rate > threshold:
            alerts.append(node)
    return alerts