from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_mains():
    return {"msg": "List of mains"}
