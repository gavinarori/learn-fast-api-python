
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from typing import List
import database
import schemas

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=schemas.ProductOut)
async def create_product(product: schemas.ProductCreate):
    product_dict = product.dict()
    result = await database.products_collection.insert_one(product_dict)
    created_product = await database.products_collection.find_one({"_id": result.inserted_id})
    created_product["_id"] = str(created_product["_id"])
    return created_product


@router.get("/", response_model=List[schemas.ProductOut])
async def get_products():
    products = []
    async for product in database.products_collection.find():
        product["_id"] = str(product["_id"])
        products.append(product)
    return products


@router.get("/{product_id}", response_model=schemas.ProductOut)
async def get_product(product_id: str):
    product = await database.products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product["_id"] = str(product["_id"])
    return product


@router.put("/{product_id}", response_model=schemas.ProductOut)
async def update_product(product_id: str, update_data: schemas.ProductUpdate):
    update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
    result = await database.products_collection.update_one(
        {"_id": ObjectId(product_id)}, {"$set": update_dict}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found or not updated")

    product = await database.products_collection.find_one({"_id": ObjectId(product_id)})
    product["_id"] = str(product["_id"])
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str):
    result = await database.products_collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
