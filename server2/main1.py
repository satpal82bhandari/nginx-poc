from fastapi import FastAPI, HTTPException
from typing import List
from models import OrderStorage
from schemas import Order, OrderCreate

app = FastAPI()
storage = OrderStorage()

@app.post("/orders/", response_model=Order)
def create_order(order_data: OrderCreate):
    return storage.create_order(order_data)

@app.get("/orders/", response_model=List[Order])
def read_orders():
    return storage.get_orders()

@app.get("/orders/{order_id}", response_model=Order)
def read_order(order_id: int):
    order = storage.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Oyrder not found")
    return order

@app.put("/orders/{order_id}", response_model=Order)
def update_order(order_id: int, order_data: OrderCreate):
    updated_order = storage.update_order(order_id, order_data)
    if updated_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    if not storage.delete_order(order_id):
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted"}
