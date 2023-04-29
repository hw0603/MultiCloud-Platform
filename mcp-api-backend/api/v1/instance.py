from fastapi import APIRouter
from service import instance_service

router = APIRouter()

@router.get("/")
def get_instance_state():
    state = instance_service.get_instance_state()
    return state
