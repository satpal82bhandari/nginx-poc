from typing import List, Optional
from schemas import Item

class ItemStorage:
    def __init__(self):
        self.items: List[Item] = []
        self.counter: int = 0

    def add_item(self, item: Item) -> Item:
        item.id = self.counter
        self.items.append(item)
        self.counter += 1
        return item

    def get_items(self) -> List[Item]:
        return self.items

    def get_item(self, item_id: int) -> Optional[Item]:
        return next((item for item in self.items if item.id == item_id), None)

    def update_item(self, item_id: int, updated_item: Item) -> Optional[Item]:
        for index, item in enumerate(self.items):
            if item.id == item_id:
                self.items[index] = updated_item
                return updated_item
        return None

    def delete_item(self, item_id: int) -> bool:
        item = self.get_item(item_id)
        if item:
            self.items.remove(item)
            return True
        return False
