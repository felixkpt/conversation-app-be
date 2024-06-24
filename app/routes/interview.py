from fastapi import APIRouter, HTTPException
from app.models.interview import interview_user

router = APIRouter()

@router.post("/interview/{sub_cat_id}/{user_id}")
async def conduct_interview(sub_cat_id: int, user_id: int):
    try:
        interview_user(sub_cat_id, user_id)
        return {"message": "Interview completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

