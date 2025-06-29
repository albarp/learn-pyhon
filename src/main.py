from fastapi import FastAPI, HTTPException
import redis
from models import ItemPayLoad

app = FastAPI()

redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

# Route to add an item
@app.post("/items/{item_name}/{quantity}")
def add_item(item_name: str, quantity: int) -> dict[str, ItemPayLoad]:
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero")
    # if the item already exists, update just the quantity
    item_id_str: str | None = redis_client.hget("item_name_to_id", item_name)
    if item_id_str is not None:
        item_id: int = int(item_id_str)
        redis_client.hincrby(f"item_id:{item_id}", "quantity", quantity)      
    # otherwise, create a new item
    else:
        item_id = redis_client.incr("item_ids")
        redis_client.hset(
            f"item_id:{item_id}",
            mapping={
                "item_id": item_id,
                "item_name": item_name,
                "quantity": quantity
            }
        )
        redis_client.hset("item_name_to_id", item_name, item_id)
    return {"item": ItemPayLoad(item_id=item_id, item_name=item_name, quantity=quantity)}

# Route to list a specific item by ID
@app.get("/items/{item_id}")
def list_item(item_id:int) -> dict[str, dict[str, str]]:
    if not redis_client.hexists(f"item_id:{item_id}", "item_id"):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": redis_client.hgetall(f"item_id:{item_id}")}

""" @app.get("/items")
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
        return {"result": f"{quantity} items removed."} """