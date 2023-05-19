from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from service import auth_service
from entity import user_entity as schemas_users

router = APIRouter()

@router.post("/access_token", response_model=schemas_users.Token)
def login_access_token(
    user_token: OAuth2PasswordRequestForm = Depends(auth_service.login_access_token),
) -> schemas_users.Token:
    return user_token