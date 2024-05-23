from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_boards():
    return {"msg": "List of boards"}
