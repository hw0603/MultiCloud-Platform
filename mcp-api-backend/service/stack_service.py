from fastapi import APIRouter, Query, Depends, HTTPException

from repository import activity_logs_repository as crud_activity
# from src.shared.helpers.get_data import check_team_stack, check_providers
from utils.utils import sync_git, copy_template
from src.shared.security import deps
from entity import stack_entity as schemas_stacks
from entity import user_entity as schemas_users
from db.connection import get_db
from repository import stack_repository as crud_stacks
from sqlalchemy.orm import Session
import logging
import random


router = APIRouter()
logger = logging.getLogger("uvicorn")


async def create_new_stack(
    stack: schemas_stacks.StackCreate,
    current_user: schemas_users.User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
):
    logger.info("create_new_stack 진입...")
    name = "default"
    environment = "default"
    team = "team"
    branch = stack.branch

    # Checkif stack name providers are supperted
    # check_providers(stack_name=stack.stack_name) TODO: 프로바이더 prefix로 validation 필요
    # logger.info("check_providers 반환...")

    # Check if stack exist
    db_stack = crud_stacks.get_stack_by_name(db, stack_name=stack.stack_name)
    logger.info("get_stack_by_name 반환...")
    if db_stack:
        raise HTTPException(
            status_code=409, detail="The stack name already exist")
    

    # Check if the user have permissions for create stack
    # check_team_stack(db, current_user, current_user.team, stack.team_access) TODO: team_access validation 필요
    # logger.info("check_team_stack 반환...")
    
    # stack_type이 지정되었다면 git에서 clone하지 않고 내부 템플릿을 복사해서 사용
    if (stack.stack_type):
        task = copy_template(
            stack_name=stack.stack_name,
            stack_type=stack.stack_type,
            environment=environment,
            team=team,
            name=name,
        )
        logger.info("copy_template 반환...")
    else:
        # Push git task to queue team, all workers are subscribed to this queue
        task = sync_git(
            stack_name=stack.stack_name,
            git_repo=stack.git_repo,
            branch=branch,
            project_path=stack.project_path,
            environment=environment,
            team=team,
            name=name,
        )
        logger.info("sync_git 반환...")
    variables_list = [i for i in task[1]["variable"].keys()]
    try:
        # DB Persistant data
        result = crud_stacks.create_new_stack(
            db=db,
            stack=stack,
            # user_id=current_user.id,
            user_id=random.randint(0, 10000000),  # TODO: user_id 넣기
            task_id=task[0],
            var_json=task[1],
            var_list=variables_list,
            team_access=stack.team_access,
        )

        crud_activity.create_activity_log(
            db=db,
            username=current_user.username,
            team=current_user.team,
            action=f"Create Stack {stack.stack_name}",
        )
        return result
    except Exception as err:
        raise HTTPException(status_code=409, detail=f"Duplicate entry {err}")


async def delete_stack_by_id_or_name(
    stack,
    current_user: schemas_users.User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
):
    try:
        if not stack.isdigit():
            result = crud_stacks.get_stack_by_name(db=db, stack_name=stack)
            if result is None:
                raise HTTPException(status_code=404, detail="Stack id not found")
            # Check if the user have permissions for delete stack
            # check_team_stack(db, current_user, current_user.team, result.team_access)

            crud_activity.create_activity_log(
                db=db,
                username=current_user.username,
                team=current_user.team,
                action=f"Delete Stack {result.stack_name}",
            )
            return crud_stacks.delete_stack_by_name(db=db, stack_name=stack)

        result = crud_stacks.get_stack_by_id(db=db, stack_id=stack)
        if result is None:
            raise HTTPException(status_code=404, detail="Stack id not found")

        # Check if the user have permissions for create stack
        # check_team_stack(db, current_user, current_user.team, result.team_access)

        crud_activity.create_activity_log(
            db=db,
            username=current_user.username,
            team=current_user.team,
            action=f"Delete Stack {result.id}",
        )
        return crud_stacks.delete_stack_by_id(db=db, stack_id=stack)
    except Exception as err:
        raise err


async def get_all_stacks(
    current_user: schemas_users.User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    # TODO: 사용자 권한 validation 필요
    # if not crud_users.is_master(db, current_user):
    #     return crud_stacks.get_all_stacks_by_team(
    #         db=db, team_access=current_user.team, skip=skip, limit=limit
    #     )
    return crud_stacks.get_all_stacks(
        db=db, skip=skip, limit=limit
    )


async def get_stack_by_id_or_name(
    stack,
    current_user: schemas_users.User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
):

    if not stack.isdigit():
        result = crud_stacks.get_stack_by_name(db=db, stack_name=stack)
        # if not crud_users.is_master(db, current_user):
        #     if result is None:
        #         raise HTTPException(
        #             status_code=404, detail="stack id not found")
        #     if (
        #         not check_team_user(current_user.team, result.team_access)
        #         and not "*" in result.team_access
        #     ):
        #         raise HTTPException(
        #             status_code=403,
        #             detail=f"Not enough permissions in {result.team_access}",
        #         )
        return result

    result = crud_stacks.get_stack_by_id(db=db, stack_id=stack)
    if result is None:
        raise HTTPException(status_code=404, detail="stack id not found")
    
    # TODO: 사용자 권한 validation 필요
    # if not crud_users.is_master(db, current_user):
    #     if (
    #         not check_team_user(current_user.team, result.team_access)
    #         and not "*" in result.team_access
    #     ):
    #         raise HTTPException(
    #             status_code=403,
    #             detail=f"Not enough permissions in {result.team_access}",
    #         )
    return result


# TODO: 내부 템플릿을 사용하는 update_stack 구현 필요
async def update_stack(
    stack_id: int,
    stack: schemas_stacks.StackCreate,
    current_user: schemas_users.User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
):
    raise NotImplementedError
    name = "default"
    environment = "default"
    team = "team"
    branch = stack.branch

    # Check if the user have permissions for create stack
    # check_team_stack(db, current_user, current_user.team, stack.team_access)
    # Checkif stack name providers are supperted
    # check_providers(stack_name=stack.stack_name)
    
    
    # Check if stack exist
    db_stack = crud_stacks.get_stack_by_id(db, stack_id=stack_id)
    
    
    # Check if stack used by deploy TODO: deploy에서 사용중인 stack은 수정 불가
    # if db_stack.stack_name != stack.stack_name:
    #     deploy = crud_deploy.get_deploy_by_stack(
    #         db=db, stack_name=db_stack.stack_name)
    #     if deploy is not None:
    #         raise HTTPException(
    #             status_code=409, detail=f"The stack is being used by {deploy.name}"
    #         )


    # Push git task to queue team, all workers are subscribed to this queue
    task = sync_git(
        stack_name=stack.stack_name,
        git_repo=stack.git_repo,
        branch=branch,
        project_path=stack.project_path,
        environment=environment,
        team=team,
        name=name,
    )
    variables_list = [i for i in task[1]["variable"].keys()]
    try:
        # pesrsist data in db
        result = crud_stacks.update_stack(
            db=db,
            stack_id=stack_id,
            stack=stack,
            user_id=current_user.id,
            task_id=task[0],
            var_json=task[1],
            var_list=variables_list,
            team_access=stack.team_access,
        )

        crud_activity.create_activity_log(
            db=db,
            username=current_user.username,
            team=current_user.team,
            action=f"Update Stack {stack.stack_name}",
        )
        return result
    except Exception as err:
        raise HTTPException(status_code=409, detail=f"Duplicate entry {err}")