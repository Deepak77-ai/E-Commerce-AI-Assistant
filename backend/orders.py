
MOCK_ORDERS = {
    "ORD123": {
        "status": "Out for delivery",
        "expected_delivery": "Today",
        "message": "Your order is out for delivery.",
    },
    "ORD456": {
        "status": "Shipped",
        "expected_delivery": "2-3 business days",
        "message": "Your order has been shipped.",
    },
    "ORD789": {
        "status": "Delivered",
        "expected_delivery": "Delivered",
        "message": "Your order has already been delivered.",
    },
}



def track_order(order_id: str) -> dict:
    """
    Look up an order and return its status.

    Args:
        order_id: The order ID entered by the customer (e.g. "ORD123").

    Returns:
        A dict with order details if found, or an error message if not.
    """

    # Normalize the input: remove spaces and make it uppercase
    # So "ord123 ", "Ord123", and "ORD123" all work the same way
    order_id = order_id.upper().strip()

    if order_id in MOCK_ORDERS:
        # Order found — return its details plus a "found: true" flag
        # The ** unpacks the order dict, so all its fields are included
        # Example response: {"found": True, "order_id": "ORD123", "status": "Shipped", ...}
        return {
            "found": True,
            "order_id": order_id,
            **MOCK_ORDERS[order_id],
        }

    # Order not found — return a helpful error message
    return {
        "found": False,
        "order_id": order_id,
        "message": "Order not found. Try ORD123, ORD456, or ORD789.",
    }