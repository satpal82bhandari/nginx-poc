# server1/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
def get_items():
    return [{"id": 1, "name": "Item1"}, {"id": 2, "name": "Item2"}]

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"id": item_id, "name": f"Item{item_id}"}
