from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from entity import deploy_detail_entity as schemas_deploy
from repository import deploy_detail_repository as crud_deploys
from db.connection import get_db
# from src.shared.helpers.get_data import (
#     check_cron_schedule,
#     check_deploy_exist,
#     check_deploy_task_pending_state,
#     check_prefix,
#     check_team_user,
#     stack,
# )
# from src.shared.helpers.push_task import (
#     async_deploy,
#     async_schedule_add,
#     async_schedule_delete,
# )
from src.shared.security import deps

from repository import task_repository as crud_tasks
from entity import user_entity as schemas_users
from repository import user_repository as crud_users


async def deploy_infra_by_stack_name(
    response: Response,
    deploy: schemas_deploy.DeployDetailCreate,
    current_user: schemas_users.User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
):

    response.status_code = status.HTTP_202_ACCEPTED
    # Get team from current user
    team = deploy.team
    # Get team from current user
    if not crud_users.is_master(db, current_user):
        current_team = current_user.team
        # if not check_team_user(current_team, [deploy.team]):
        #     raise HTTPException(
        #         status_code=403, detail=f"Not enough permissions in {team}"
        #     )







    
    return deploy.variables


    
    # Get  credentials by providers supported
    secreto = check_prefix(
        db, stack_name=deploy.stack_name, environment=deploy.environment, team=team
    )
    # Get info from stack data
    stack_data = stack(db, stack_name=deploy.stack_name)
    branch = (
        stack_data.branch
        if deploy.stack_branch == "" or deploy.stack_branch == None
        else deploy.stack_branch
    )
    git_repo = stack_data.git_repo
    tf_ver = stack_data.tf_version
    check_deploy_exist(db, deploy.name, team,
                       deploy.environment, deploy.stack_name)
    check_deploy_task_pending_state(deploy.name, team, deploy.environment)
    try:
        # check crontime
        check_cron_schedule(deploy.start_time)
        check_cron_schedule(deploy.destroy_time)
        # push task Deploy to queue and return task_id
        pipeline_deploy = async_deploy(
            git_repo,
            deploy.name,
            deploy.stack_name,
            deploy.environment,
            team,
            branch,
            tf_ver,
            deploy.variables,
            secreto,
            deploy.tfvar_file,
            deploy.project_path,
            current_user.username,
        )
        # Push deploy task data
        db_deploy = crud_deploys.create_new_deploy(
            db=db,
            deploy=deploy,
            stack_branch=branch,
            task_id=pipeline_deploy,
            action="Apply",
            team=team,
            user_id=current_user.id,
            username=current_user.username,
        )
        # Push task data
        db_task = crud_tasks.create_task(
            db=db,
            task_id=pipeline_deploy,
            task_name=f"{deploy.stack_name}-{team}-{deploy.environment}-{deploy.name}",
            user_id=current_user.id,
            deploy_id=db_deploy.id,
            username=current_user.username,
            team=team,
            action="Apply",
        )

        return {"task": db_task}
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"{err}")
    finally:
        try:
            # async_schedule_delete(db_deploy.id, team)
            # # Add schedule
            # async_schedule_add(db_deploy.id, team)
            ...
        except Exception as err:
            print(err)
