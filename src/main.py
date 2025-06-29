from fastapi import FastAPI, HTTPException
from models import ItemPayLoad

app = FastAPI()

grocery_list: dict[int, ItemPayLoad] = {}

@app.post("/items/{item_name}/{quantity}")
def add_item(item_name: str, quantity: int) -> dict[str, ItemPayLoad]:
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero")
    # if the item already exists, update just the quantity
    items_ids: dict[str, int] = {item.item_name: item.item_id if item.item_id is not None else 0 for item in grocery_list.values()}
    if item_name in items_ids.keys():
        # get index of item_name in item_ids, which is the item_id
        item_id = items_ids[item_name]
        grocery_list[item_id].quantity += quantity
    # otherwise, create a new item
    else:
        item_id: int = max(grocery_list.keys()) + 1 if grocery_list else 0
        grocery_list[item_id] = ItemPayLoad(
            item_id=item_id,
            item_name=item_name,
            quantity=quantity
        )
    return {"item": grocery_list[item_id]}
