from sqlalchemy import inspect
from src.worker.tasks.terraform_worker import (
    # output,
    # pipeline_deploy,
    # pipeline_destroy,
    pipeline_git_pull,
    pipeline_copy_template,
    # pipeline_plan,
    # schedule_add,
    # schedule_delete,
    # schedule_get,
    # schedule_update,
    # schedules_list,
    # show,
    # unlock,
)
from repository import user_repository as crud_users
import json
from fastapi import APIRouter, Depends, HTTPException, Query

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def sync_git(
    stack_name: str,
    git_repo: str,
    branch: str,
    project_path: str,
    environment: str,
    team: str,
    name: str,
):
    try:
        pipeline_git_result = pipeline_git_pull.s(
            stack_name=stack_name,
            git_repo=git_repo,
            branch=branch,
            project_path=project_path,
            environment=environment,
            team=team,
            name=name,
        ).apply_async(queue="team")
        task_id = pipeline_git_result.task_id
        get_data = pipeline_git_result.get()
        try:
            data = json.loads(get_data.get("stdout"))
        except Exception:
            raise ValueError(get_data.get("result"))
        return task_id, data
    except Exception as err:
        raise HTTPException(status_code=408, detail=f"{err}")

def copy_template(
    stack_name: str,
    stack_type: str,
    environment: str,
    team: str,
    name: str,
):
    try:
        pipeline_copy_result = pipeline_copy_template.s(
            stack_name=stack_name,
            stack_type=stack_type,
            environment=environment,
            team=team,
            name=name,
        ).apply_async(queue="team")
        task_id = pipeline_copy_result.task_id
        get_data = pipeline_copy_result.get()
        try:
            data = json.loads(get_data.get("stdout"))
        except Exception:
            raise ValueError(get_data.get("result"))
        return task_id, data
    except Exception as err:
        raise HTTPException(status_code=408, detail=f"{err}")


def check_supported_csp(csp_type: str) -> bool:
    csp_supported = {"aws", "azure", "gcp", "custom"}
    return csp_type in csp_supported


def check_team_stack(
    db, current_user: str, current_user_team: list, stack_team_access: list
) -> bool:
    if not crud_users.is_master(db, current_user):
        if ("team_manager" not in current_user.role):
            raise HTTPException(
                status_code=403, detail=f"스택을 생성하기 위한 권한이 없습니다."
            )
        if ("*" in stack_team_access and "system_manager" not in current_user.role):
            raise HTTPException(
                status_code=403,
                detail="system_manager가 아니라면 *(와일드카드)를 사용할 수 없습니다.)",
            )
        if not all(__team in current_user_team for __team in stack_team_access):
            raise HTTPException(
                status_code=403,
                detail=f"요청한 팀 중 권한이 없는 팀이 있습니다. {stack_team_access}",
            )