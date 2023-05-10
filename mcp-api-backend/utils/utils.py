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
