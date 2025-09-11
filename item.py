from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.db import collections
from bson.objectid import ObjectId
from backend.utils import serialize_document

router = APIRouter()

# MongoDB collection
item_collection = collections["items"]

# Pydantic model
class Item(BaseModel):
    name: str

# Create a new item
@router.post("/items", status_code=201)
async def create_item(item: Item):
    if not item.name:
        raise HTTPException(status_code=400, detail="Name is required")
    try:
        new_item = {"name": item.name}
        result = item_collection.insert_one(new_item)
        return {"id": str(result.inserted_id), "name": item.name}
    except Exception:
        raise HTTPException(status_code=500, detail="Database Error!")

# Get all items
@router.get("/items")
async def get_items():
    try:
        items = list(item_collection.find())
        return [serialize_document(item) for item in items]
    except Exception:
        raise HTTPException(status_code=500, detail="Invalid Request")

# Update an item by ID
@router.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    if not item.name:
        raise HTTPException(status_code=400, detail="Name is required")
    try:
        result = item_collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": {"name": item.name}}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"id": item_id, "name": item.name}
    except Exception:
        raise HTTPException(status_code=500, detail="Database Error!")

# Delete an item by ID
@router.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: str):
    try:
        result = item_collection.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return
    except Exception:
        raise HTTPException(status_code=500, detail="Database Error!")
