from fastapi import FastAPI, HTTPException
from models import ItemPayLoad

app = FastAPI()

grocery_list: dict[int, ItemPayLoad] = {}

# Route to add an item
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

# Route to list a specific item by ID
@app.get("/items/{item_id}")
def list_item(item_id:int) -> dict[str, ItemPayLoad]:
    if item_id not in grocery_list:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": grocery_list[item_id]}

@app.get("/items")
def list_items() -> dict[str, dict[int, ItemPayLoad]]:
    return {"items": grocery_list}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in grocery_list:
        raise HTTPException(status_code=404, detail="Item not found")
    del grocery_list[item_id]
    return {"message": "Item deleted"}

@app.delete("/items/{item_id}/{quantity}")
def remove_quantity(item_id: int, quantity: int):
    if item_id not in grocery_list:
        raise HTTPException(status_code=404, detail="Item not found")
    if grocery_list[item_id].quantity < quantity:
        del grocery_list[item_id]
        return {"message": "Item deleted"}
    else:
        grocery_list[item_id].quantity -= quantity
        return {"result": f"{quantity} items removed."}