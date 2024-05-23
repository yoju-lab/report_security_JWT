from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_securities():
    return {"msg": "List of securities"}
