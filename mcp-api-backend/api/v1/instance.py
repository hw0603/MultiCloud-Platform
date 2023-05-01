from fastapi import APIRouter
from service import instance_service
from api.api_response import *
from config.api_config import settings  # for testing

router = APIRouter()

@router.get("/")
def get_instance_state():
    state = instance_service.get_instance_state()
    return state

@router.get("/list")
def get_instance_list():
    ''' Authentication 추가 후에는 각 프로바이더의 인증 정보를 가져와서 사용할 것 '''
    AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
    AWS_DEFAULT_REGION = 'ap-northeast-2'

    instance_list = instance_service.get_instance_list(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION)
    return ApiResponse.with_data(ApiStatus.SUCCESS, "success", instance_list)
