from fastapi import FastAPI
from typing import Dict, Any

app = FastAPI()

# Root endpoint
# Purpose: Health check to verify API is running
# Method: GET
# Returns: Simple JSON message
@app.get("/")
def read_root():
    return {"message": "API running"}


# Item retrieval endpoint
# Purpose: Fetch an item using its ID
# Method: GET
# Path Parameter:
#   - items_id (int): must be an integer, otherwise FastAPI returns 422
# Query Parameter:
#   - q (str | None): optional search/filter string
@app.get("/items/{items_id}")
def read_item(items_id: int, q: str | None = None):
    return {
        "item_id": items_id,
        "query": q
    }


# Item creation endpoint
# Purpose: Create a new item
# Method: POST
# Request Body:
#   - item (dict): JSON payload sent by client
# Notes:
#   - If body is missing or invalid, FastAPI returns 422
@app.post("/items/")
def create_item(item: Dict[str, Any]):
    return {
        "created_item": item
    }


# Search endpoint
# Purpose: Perform search based on query string
# Method: GET
# Query Parameter:
#   - query (str): required search keyword
@app.get("/search")
def search_items(query: str):
    return {
        "results": f"Results for query: {query}"
    }
