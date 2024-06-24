from fastapi import APIRouter, HTTPException
from app.models.conversation import (
    reset_messages, archive_messages
)
from app.models.category import (
    get_cat_conversation
)
from app.models.subcategory import (
    get_sub_cat_conversation
)

router = APIRouter()


@router.get("/dashboard/categories/{cat_id}/conversation")
async def cat_conversation(cat_id: str):
    conversation = get_cat_conversation(cat_id)
    return conversation


@router.get("/dashboard/sub-categories/{sub_cat_id}/conversation")
async def sub_cat_conversation(sub_cat_id: str):
    conversation = get_sub_cat_conversation(sub_cat_id)
    return conversation


@router.get("/reset-conversation")
async def reset_conversation(cat_id: str):
    reset_messages(cat_id)
    return {"message": "Conversation reset."}


@router.put("/dashboard/categories/{cat_id}/sub-categories/{sub_cat_id}/archive")
async def archive_conversation(cat_id: int, sub_cat_id: int):
    try:
        archive_messages(cat_id, sub_cat_id)
        return {"message": "Conversation archived successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to archive conversation: {e}")
