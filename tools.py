from dataclasses import dataclass

ORDERS = {
    "ORD-1001":"shipped","ORD-1002":"processing","ORD-1003":"delivered",
    "ORD-1004":"processing","ORD-1005":"pending-review","ORD-1006":"processing"
}

@dataclass
class AuthorizationContext:
    allow_read_orders: bool = True
    allow_side_effects: bool = False

def get_order_status(order_id: str, auth: AuthorizationContext) -> dict:
    if not auth.allow_read_orders:
        raise PermissionError("Order read not authorized")
    return {"order_id": order_id, "status": ORDERS.get(order_id, "unknown")}
