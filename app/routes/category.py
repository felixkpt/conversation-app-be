from fastapi import APIRouter, HTTPException
from app.schemas.category import CategoryRequest
from app.models.category import (
    get_cats, category_exists, get_cat, add_category, update_category,
)
from app.services.helpers import format_error


router = APIRouter()

@router.get("/dashboard/categories")
async def categories():
    cats = get_cats()
    return cats


@router.get("/dashboard/categories/{cat_id}")
async def get_category(cat_id: str):
    cat = get_cat(cat_id)
    return cat


@router.post("/dashboard/categories")
async def create_category(category: CategoryRequest):
    if category_exists(category.name):
        raise HTTPException(status_code=400, detail=format_error(
            "name", "Category already exists."))
    try:
        add_category(category.name, category.description)
        return {"message": "Category added successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to add category: {e}")


@router.put("/dashboard/categories/{category_id}")
async def update_category_endpoint(category_id: int, category: CategoryRequest):
    existing_category = get_cat(category_id)
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")
    try:
        update_category(category_id, category)
        return {"message": "Category updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update category: {e}")
