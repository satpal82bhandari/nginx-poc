from typing import List, Optional
from schemas import Order, OrderCreate
from datetime import datetime

class OrderStorage:
    def __init__(self):
        self.orders: List[Order] = []
        self.counter: int = 1

    def create_order(self, order_data: OrderCreate) -> Order:
        new_order = Order(
            id=self.counter,
            item_name=order_data.item_name,
            quantity=order_data.quantity,
            total_price=order_data.total_price,
            created_at=datetime.utcnow(),
        )
        self.orders.append(new_order)
        self.counter += 1
        return new_order

    def get_orders(self) -> List[Order]:
        return self.orders

    def get_order(self, order_id: int) -> Optional[Order]:
        return next((order for order in self.orders if order.id == order_id), None)

    def update_order(self, order_id: int, order_data: OrderCreate) -> Optional[Order]:
        order = self.get_order(order_id)
        if order:
            order.item_name = order_data.item_name
            order.quantity = order_data.quantity
            order.total_price = order_data.total_price
            order.updated_at = datetime.utcnow()
            return order
        return None

    def delete_order(self, order_id: int) -> bool:
        order = self.get_order(order_id)
        if order:
            self.orders.remove(order)
            return True
        return False
