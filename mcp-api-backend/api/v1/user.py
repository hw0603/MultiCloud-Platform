from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from service.user import user_service
from entity.user_entity import (
    User,
    UserInit,
    UserCreate,
    UserUpdate
)

router = APIRouter()

@router.post("/start", response_model=User)
async def create_init_user(
    create_init_user: UserInit = Depends(user_service.create_init_user),
):
    return create_init_user

@router.post("/", response_model=User)
async def create_user(create_user: UserCreate = Depends(user_service.create_user)):
    return create_user

@router.get("/")
async def get_user_list(get_user_list: User = Depends(user_service.get_user_list)):
    return get_user_list

@router.patch("/{user_id}", response_model=User)
async def update_user(update_user: UserUpdate = Depends(user_service.update_user)):
    return update_user
