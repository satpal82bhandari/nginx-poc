from fastapi import FastAPI, HTTPException
from typing import List
from models import ItemStorage
from schemas import Item

app = FastAPI()
storage = ItemStorage()

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    return storage.add_item(item)

@app.get("/items/", response_model=List[Item])
def read_items():
    return storage.get_items()

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    item = storage.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    updated_item = storage.update_item(item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if not storage.delete_item(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "Item deleted"}
