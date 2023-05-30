from fastapi import APIRouter, Query, Depends, HTTPException

from repository import activity_logs_repository as crud_activity
# from src.shared.helpers.get_data import check_team_stack, check_providers
from utils.utils import sync_git, copy_template, check_supported_csp, check_team_stack
from src.shared.security import deps
from entity import stack_entity as schemas_stacks
from entity import user_entity as schemas_users
from db.connection import get_db
from repository import stack_repository as crud_stacks
from repository import user_repository as crud_users
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

    # 지원하는 CSP인지 확인
    if not (check_supported_csp(stack.csp_type)):
        raise HTTPException(status_code=409, detail=f"{stack.csp_type} 는 지원하지 않는 CSP입니다.")

    # 스택이 존재하는지 확인
    db_stack = crud_stacks.get_stack_by_name(db, stack_name=stack.stack_name)
    if (db_stack):
        raise HTTPException(status_code=409, detail="해당 스택 이름이 이미 존재합니다.")
    

    # 현재 사용자가 스택을 생성할 권한이 있는지 확인
    check_team_stack(db, current_user, current_user.team, stack.team_access)
    
    # stack_type이 지정되었다면 git에서 clone하지 않고 내부 템플릿을 복사해서 사용
    if (stack.stack_type):
        task = copy_template(
            stack_name=stack.stack_name,
            stack_type=stack.stack_type,
            csp_type=stack.csp_type,
            environment=environment,
            team=team,
            name=name,
        )
    else:
        # Git task를 'team' 큐에 푸시하고, 모든 워커는 이 큐에 subscribed 되어 있음
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
        # DB Persistant data
        result = crud_stacks.create_new_stack(
            db=db,
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
            action=f"스택 {stack.stack_name} 생성",
        )
        return result
    except Exception as err:
        raise HTTPException(status_code=409, detail=f"엔트리 중복: {err}")


async def delete_stack_by_id_or_name(
    stack,
    current_user: schemas_users.User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
):
    try:
        if not (stack.isdigit()):
            result = crud_stacks.get_stack_by_name(db=db, stack_name=stack)
            if result is None:
                raise HTTPException(status_code=404, detail="스택 ID를 찾을 수 없습니다.")
            
            # TODO: 현재 유저가 스택을 삭제할 권한이 있는지 확인
            # check_team_stack(db, current_user, current_user.team, result.team_access)

            crud_activity.create_activity_log(
                db=db,
                username=current_user.username,
                team=current_user.team,
                action=f"스택 {result.stack_name} 삭제",
            )
            return crud_stacks.delete_stack_by_name(db=db, stack_name=stack)

        result = crud_stacks.get_stack_by_id(db=db, stack_id=stack)
        if (result is None):
            raise HTTPException(status_code=404, detail="스택 ID를 찾을 수 없습니다.")

        # TODO: 현재 유저가 스택을 삭제할 권한이 있는지 확인
        # check_team_stack(db, current_user, current_user.team, result.team_access)

        crud_activity.create_activity_log(
            db=db,
            username=current_user.username,
            team=current_user.team,
            action=f"스택 {result.id} 삭제",
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

    if not crud_users.is_master(db, current_user):
        return crud_stacks.get_all_stacks_by_team(
            db=db, team_access=current_user.team, skip=skip, limit=limit
        )
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
        if not crud_users.is_master(db, current_user):
            if result is None:
                raise HTTPException(
                    status_code=404, detail="스택 ID를 찾을 수 없습니다.")
            if (
                # not check_team_user(current_user.team, result.team_access) and 
                not "*" in result.team_access
            ):
                raise HTTPException(
                    status_code=403,
                    detail=f"{result.team_access} 에 접근 권한이 없습니다.",
                )
        return result

    result = crud_stacks.get_stack_by_id(db=db, stack_id=stack)
    if result is None:
        raise HTTPException(status_code=404, detail="스택 ID를 찾을 수 없습니다.")
    
    if not crud_users.is_master(db, current_user):
        if (
            # not check_team_user(current_user.team, result.team_access) and
            not "*" in result.team_access
        ):
            raise HTTPException(
                status_code=403,
                detail=f"{result.team_access} 에 접근 권한이 없습니다.",
            )
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
