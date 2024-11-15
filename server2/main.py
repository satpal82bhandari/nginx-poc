# server2/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/orders/")
def get_orders():
    return [{"id": 1, "item": "Item1", "quantity": 2}]

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    return {"id": order_id, "item": f"Item{order_id}", "quantity": 3}
