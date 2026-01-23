from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# -----------------------------
# Pydantic Model (Request Schema)
# -----------------------------
# This model defines the expected structure of input data.
# FastAPI validates incoming request bodies against this schema
# BEFORE the request reaches business logic.
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


# -----------------------------
# Root Endpoint
# -----------------------------
# Purpose: Health check endpoint to verify API availability.
@app.get("/")
async def read_root():
    return {"status": "API is running"}


# -----------------------------
# POST Endpoint (Raw Response)
# -----------------------------
# Purpose:
# - Accept item data
# - Demonstrate request body validation
# - Show manual response shaping using dict operations
#
# Note:
# - This endpoint does NOT enforce a strict response contract
# - Used for understanding behavior, not ideal for production
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()

    # Compute derived field only if tax is provided
    if item.tax is not None:
        total_price = item.price + item.tax
        item_dict.update({"total_price": total_price})
    else:
        item_dict.update({"tax": "No tax provided"})

    # Add default value when optional field is missing
    if item.description is None:
        item_dict.update({"description": "No description provided"})

    return item_dict


# -----------------------------
# PUT Endpoint (Path + Query + Body)
# -----------------------------
# Purpose:
# - Demonstrates combination of:
#   - Path parameters
#   - Query parameters
#   - Request body
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    if q:
        return {
            "item_id": item_id,
            "q": q,
            **item.model_dump()
        }
    return {
        "item_id": item_id,
        **item.model_dump()
    }


# -----------------------------
# Pydantic Model (Response Schema)
# -----------------------------
# This model defines what the client is allowed to see.
# Any extra fields returned by the function are filtered out.
class ItemResponse(BaseModel):
    name: str
    description: str | None = None
    price: float
    total_price: float | None = None


# -----------------------------
# POST Endpoint (Controlled Response)
# -----------------------------
# Purpose:
# - Demonstrates response_model usage
# - Enforces output contract
# - Hides internal fields from clients
@app.post("/items/response/", response_model=ItemResponse)
async def create_item_response(item: Item):
    total_price = None
    if item.tax is not None:
        total_price = item.price + item.tax

    # Even though we return extra fields,
    # FastAPI filters the response using ItemResponse
    return {
        "name": item.name,
        "price": item.price,
        "total_price": total_price,
        "internal_note": "This field is not visible"
    }
