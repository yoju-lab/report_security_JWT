from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_users():
    return {"msg": "List of users"}
