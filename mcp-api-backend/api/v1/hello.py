from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def hello_world():
    """
    API 설명
    """
    return "Hello World"
