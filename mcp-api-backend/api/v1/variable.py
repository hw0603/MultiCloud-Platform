from fastapi import APIRouter, Depends


router = APIRouter()


@router.get("/json")
async def get_json(
    stack_json: dict# = Depends(...),
):
    return stack_json


@router.get("/list")
async def get_list(
    stack_list: list# = Depends(...),
):
    return stack_list


# @router.get("/deploy/{deploy_id}")
# async def get_deploy_by_id(
#     deploy_variables: dict = Depends(...),
# ):
#     return deploy_variables
