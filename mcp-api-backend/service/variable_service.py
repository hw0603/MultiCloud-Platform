from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

# from src.deploy.infrastructure import repositories as crud_deploys
# from src.shared.helpers.get_data import check_team_user
from src.shared.security import deps
from db.connection import get_db
from repository import stack_repository as crud_stacks
from entity import user_entity as schemas_users
from repository import user_repository as crud_users


async def get_json(
    stack,
    current_user: schemas_users.User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    스택의 이름 또는 id를 전달하면 스택 내의 변수들을 JSON으로 반환
    """
    try:
        if stack.isdigit():
            result = crud_stacks.get_stack_by_id(db=db, stack_id=stack)
            if result == None:
                raise HTTPException(
                    status_code=404, detail=f"Not found"
                )
            # TODO: team_access에 대한 권한 체크
            # if not crud_users.is_master(db, current_user):
            #     if "*" not in result.team_access:
            #         if not check_team_user(current_user.team, result.team_access):
            #             raise HTTPException(
            #                 status_code=403, detail=f"Not enough permissions"
            #             )
            return result.var_json.get("variable")
        else:
            result = crud_stacks.get_stack_by_name(db=db, stack_name=stack)
            if result == None:
                raise HTTPException(
                    status_code=404, detail=f"Not found"
                )
            # if not crud_users.is_master(db, current_user):
            #     if "*" not in result.team_access:
            #         if not check_team_user(current_user.team, result.team_access):
            #             raise HTTPException(
            #                 status_code=403, detail=f"Not enough permissions"
            #             )
            return result.var_json.get("variable")
    except Exception as err:
        raise err


async def get_list(
    stack,
    current_user: schemas_users.User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    스택의 이름 또는 id를 전달하면 스택 내의 변수들을 리스트 형태로 반환
    """
    try:
        if stack.isdigit():
            result = crud_stacks.get_stack_by_id(db=db, stack_id=stack)
            if result == None:
                raise HTTPException(
                    status_code=404, detail=f"Not found"
                )
            # if not crud_users.is_master(db, current_user):
            #     if "*" not in result.team_access:
            #         if not check_team_user(current_user.team, result.team_access):
            #             raise HTTPException(
            #                 status_code=403, detail=f"Not enough permissions"
            #             )
            return result.var_list
        else:
            result = crud_stacks.get_stack_by_name(db=db, stack_name=stack)
            if result == None:
                raise HTTPException(
                    status_code=404, detail=f"Not found"
                )
            # if not crud_users.is_master(db, current_user):
            #     if "*" not in result.team_access:
            #         if not check_team_user(current_user.team, result.team_access):
            #             raise HTTPException(
            #                 status_code=403, detail=f"Not enough permissions"
            #             )
            return result.var_list
    except Exception as err:
        raise err


# async def get_deploy_by_id(
#     deploy_id: int,
#     current_user: schemas_users.User = Depends(deps.get_current_active_user),
#     db: Session = Depends(get_db),
# ):

#     try:
#         result = crud_deploys.get_deploy_by_id(db=db, deploy_id=deploy_id)
#         if result == None:
#             raise HTTPException(
#                 status_code=404, detail=f"Not found"
#             )
#         if not crud_users.is_master(db, current_user):
#             if not check_team_user(current_user.team, [result.team]):
#                 raise HTTPException(
#                     status_code=403, detail=f"Not enough permissions"
#                 )
#         return result.variables
#     except Exception as err:
#         raise err
