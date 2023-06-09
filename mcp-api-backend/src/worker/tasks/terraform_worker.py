import logging
import traceback

import redis
from celery import states
from celery.exceptions import Ignore
from celery.utils.log import get_task_logger
from config.api_config import settings
from config.celery_config import celery_app

from src.worker.provider import ProviderActions, ProviderGetVars, ProviderRequirements
# from src.worker.tasks.helpers.folders import Utils
# from src.worker.tasks.helpers.metrics import push_metric
# from src.worker.tasks.helpers.schedule import request_url

# r = redis.Redis(
#     host=settings.BACKEND_SERVER,
#     port=6379,
#     db=2,
#     charset="utf-8",
#     decode_responses=True,
# )

logger = get_task_logger(__name__)


# @celery_app.task(
#     bind=True, acks_late=True, time_limit=settings.DEPLOY_TMOUT, name="pipeline Deploy"
# )
# @push_metric()
# def pipeline_deploy(
#     self,
#     git_repo: str,
#     name: str,
#     stack_name: str,
#     environment: str,
#     team: str,
#     branch: str,
#     version: str,
#     kwargs: any,
#     secreto: str,
#     variables_file: str = "",
#     project_path: str = "",
#     user: str = "",
# ):
#     try:
#         logger.info(
#             f"[DEPLOY] User {user} launch deploy {name} with stack {stack_name} on team {team} and environment {environment}"
#         )
#         r.set(f"{name}-{team}-{environment}", "Locked")
#         logger.info(f"[DEPLOY] lock sld {name}-{team}-{environment}")
#         r.expire(f"{name}-{team}-{environment}", settings.TASK_LOCKED_EXPIRED)
#         logger.info(
#             f"[DEPLOY] set sld {name}-{team}-{environment} expire timeout {settings.TASK_LOCKED_EXPIRED}"
#         )
#         # Git clone repo
#         logger.info(
#             f"[DEPLOY] User {user} launch deploy {name} with stack {stack_name} on team {team} and environment {environment} git pull"
#         )
#         result = ProviderRequirements.artifact_download(
#             name, stack_name, environment, team, git_repo, branch
#         )

#         self.update_state(state="PULLING", meta={"done": "1 of 6"})
#         if result["rc"] != 0:
#             logger.error(
#                 f"[DEPLOY] Error when user {user} launch deploy {name} with stack {stack_name} on team {team} and environment {environment} git pull"
#             )
#             raise Exception(result)
#         # Download terrafom
#         logger.info(
#             f"[DEPLOY] User {user} launch deploy {name} with stack {stack_name} on team {team} and environment {environment} download terrafom version {version}"
#         )
#         result = ProviderRequirements.binary_download(version)

#         self.update_state(state="LOADBIN", meta={"done": "2 of 6"})
#         # Delete artifactory to avoid duplicating the runner logs
#         if result["rc"] != 0:
#             logger.error(
#                 f"[DEPLOY] Error when User {user} launch deploy {name} with stack {stack_name} on team {team} and environment {environment} download terrafom version {version}"
#             )
#             raise Exception(result)

#         # Create tf to use the custom backend state
#         self.update_state(state="REMOTECONF", meta={"done": "3 of 6"})

#         result = ProviderRequirements.storage_state(
#             name, stack_name, environment, team, project_path
#         )
#         if result["rc"] != 0:
#             raise Exception(result)

#         # Create tfvar serialize with json
#         self.update_state(state="SETVARS", meta={"done": "4 of 6"})
#         result = ProviderRequirements.parameter_vars(
#             name, stack_name, environment, team, project_path, kwargs
#         )
#         if result["rc"] != 0:
#             raise Exception(result)
#         # Plan execute
#         logger.info(
#             f"[DEPLOY] User {user} launch deploy {name} with stack {stack_name} on team {team} and environment {environment} terraform plan"
#         )
#         self.update_state(state="PLANNING", meta={"done": "5 of 6"})
#         result = ProviderActions.plan(
#             name,
#             stack_name,
#             branch,
#             environment,
#             team,
#             version,
#             secreto,
#             variables_file,
#             project_path,
#         )

#         if result["rc"] != 0:
#             logger.error(
#                 f"[DEPLOY] Error when User {user} launch deploy {name} with stack {stack_name} on team {team} and environment {environment} execute terraform plan"
#             )
#             raise Exception(result)
#         # Apply execute
#         logger.info(
#             f"[DEPLOY] User {user} launch deploy {name} with stack {stack_name} on team {team} and environment {environment} terraform apply with timeout deploy setting {settings.DEPLOY_TMOUT}"
#         )
#         self.update_state(state="APPLYING", meta={"done": "6 of 6"})
#         result = ProviderActions.apply(
#             name,
#             stack_name,
#             branch,
#             environment,
#             team,
#             version,
#             secreto,
#             variables_file,
#             project_path,
#         )
#         if result["rc"] != 0:
#             logger.error(
#                 f"[DEPLOY] Error when User {user} launch deploy {name} with stack {stack_name} on team {team} and environment {environment} download terrafom version {version}"
#             )
#             raise Exception(result)
#         return result
#     except Exception as err:
#         if not settings.ROLLBACK:
#             logger.error(
#                 f"[DEPLOY] Error when User {user} launch deploy {name} with stack {stack_name} on team {team} and environment {environment} download terrafom version {version} execute Retry"
#             )
#             self.retry(
#                 countdown=settings.TASK_RETRY_INTERVAL,
#                 exc=err,
#                 max_retries=settings.TASK_MAX_RETRY,
#             )
#             self.update_state(state=states.FAILURE, meta={"exc": result})
#             raise Ignore()
#             logger.error(
#                 f"[DEPLOY] Error when User {user} launch deploy {name} with stack {stack_name} on team {team} and environment {environment} download terrafom version {version} execute RollBack"
#             )
#         self.update_state(state="ROLLBACK", meta={"done": "1 of 1"})
#         destroy_result = ProviderActions.destroy(
#             name,
#             stack_name,
#             branch,
#             environment,
#             team,
#             version,
#             secreto,
#             variables_file,
#             project_path,
#         )
#         self.update_state(
#             state=states.FAILURE,
#             meta={
#                 "exc_type": type(err).__name__,
#                 "exc_message": traceback.format_exc().split("\n"),
#             },
#         )
#         raise Ignore()
#     finally:
#         dir_path = f"/tmp/{ stack_name }/{environment}/{team}/{name}"
#         r.delete(f"{name}-{team}-{environment}")
#         if not settings.DEBUG:
#             Utils.delete_local_folder(dir_path)


# @celery_app.task(bind=True, acks_late=True, name="pipeline Destroy")
# @push_metric()
# def pipeline_destroy(
#     self,
#     git_repo: str,
#     name: str,
#     stack_name: str,
#     environment: str,
#     team: str,
#     branch: str,
#     version: str,
#     kwargs: any,
#     secreto: str,
#     variables_file: str = "",
#     project_path: str = "",
#     user: str = "",
# ):
#     try:
#         logger.info(
#             f"User {user} launch destroy {name} with stack {stack_name} on team {team} and environment {environment}"
#         )
#         r.set(f"{name}-{team}-{environment}", "Locked")
#         logger.info(f"lock sld {name}-{team}-{environment}")
#         r.expire(f"{name}-{team}-{environment}", settings.TASK_LOCKED_EXPIRED)
#         logger.info(
#             f"set sld {name}-{team}-{environment} expire timeout {settings.TASK_LOCKED_EXPIRED}"
#         )
#         # Git clone repo
#         logger.info(
#             f"User {user} Destroy deploy {name} with stack {stack_name} on team {team} and environment {environment} git pull"
#         )
#         result = ProviderRequirements.artifact_download(
#             name, stack_name, environment, team, git_repo, branch
#         )
#         self.update_state(state="PULLING", meta={"done": "1 of 6"})
#         if result["rc"] != 0:
#             raise Exception(result)
#         # Download terrafom
#         logger.info(
#             f"User {user} Destroy deploy {name} with stack {stack_name} on team {team} and environment {environment} download terrafom version {version}"
#         )
#         result = ProviderRequirements.binary_download(version)
#         self.update_state(state="LOADBIN", meta={"done": "2 of 6"})
#         # Delete artifactory to avoid duplicating the runner logs
#         if result["rc"] != 0:
#             logger.error(
#                 f"Error when User {user} launch destroy {name} with stack {stack_name} on team {team} and environment {environment} download terrafom version {version}"
#             )
#             raise Exception(result)
#         # Create tf to use the custom backend storage state
#         self.update_state(state="REMOTECONF", meta={"done": "3 of 6"})
#         result = ProviderRequirements.storage_state(
#             name, stack_name, environment, team, project_path
#         )
#         if result["rc"] != 0:
#             raise Exception(result)
#         # Create tfvar serialize with json
#         self.update_state(state="SETVARS", meta={"done": "4 of 6"})
#         result = ProviderRequirements.parameter_vars(
#             name, stack_name, environment, team, project_path, kwargs
#         )
#         if result["rc"] != 0:
#             raise Exception(result)

#         logger.info(
#             f"User {user} launch destroy {name} with stack {stack_name} on team {team} and environment {environment} execute destroy"
#         )
#         self.update_state(state="DESTROYING", meta={"done": "6 of 6"})
#         result = ProviderActions.destroy(
#             name,
#             stack_name,
#             branch,
#             environment,
#             team,
#             version,
#             secreto,
#             variables_file,
#             project_path,
#         )
#         if result["rc"] != 0:
#             raise Exception(result)
#         return result
#     except Exception as err:
#         self.retry(countdown=5, exc=err, max_retries=1)
#         self.update_state(state=states.FAILURE, meta={"exc": result})
#         raise Ignore()
#     finally:
#         dir_path = f"/tmp/{ stack_name }/{environment}/{team}/{name}"
#         Utils.delete_local_folder(dir_path)
#         r.delete(f"{name}-{team}-{environment}")


# @celery_app.task(bind=True, acks_late=True, name="pipeline Plan")
# @push_metric()
# def pipeline_plan(
#     self,
#     git_repo: str,
#     name: str,
#     stack_name: str,
#     environment: str,
#     team: str,
#     branch: str,
#     version: str,
#     kwargs: any,
#     secreto: str,
#     variables_file: str = "",
#     project_path: str = "",
#     user: str = "",
# ):
#     try:
#         r.set(f"{name}-{team}-{environment}", "Locked")
#         logger.info(f"[DEPLOY] lock sld {name}-{team}-{environment}")
#         r.expire(f"{name}-{team}-{environment}", settings.TASK_LOCKED_EXPIRED)
#         logger.info(
#             f"User {user} launch plan {name} with stack {stack_name} on team {team} and environment {environment}"
#         )
#         self.update_state(state="GIT", meta={"done": "1 of 5"})
#         result = ProviderRequirements.artifact_download(
#             name, stack_name, environment, team, git_repo, branch
#         )
#         if result["rc"] != 0:
#             logger.error(
#                 f"Error when user {user} launch plan {name} with stack {stack_name} on team {team} and environment {environment} git pull"
#             )
#             raise Exception(result)
#         self.update_state(state="BINARY", meta={"done": "2 of 5"})
#         logger.info(
#             f"User {user} launch plan {name} with stack {stack_name} on team {team} and environment {environment} download terrafom version {version}"
#         )
#         result = ProviderRequirements.binary_download(version)
#         if result["rc"] != 0:
#             logger.error(
#                 f"Error when User {user} launch plan {name} with stack {stack_name} on team {team} and environment {environment} download terrafom version {version}"
#             )
#             raise Exception(result)

#         self.update_state(state="REMOTE", meta={"done": "3 of 5"})
#         result = ProviderRequirements.storage_state(
#             name, stack_name, environment, team, project_path
#         )
#         if result["rc"] != 0:
#             raise Exception(result)

#         self.update_state(state="VARS", meta={"done": "4 of 5"})
#         result = ProviderRequirements.parameter_vars(
#             name, stack_name, environment, team, project_path, kwargs
#         )
#         if result["rc"] != 0:
#             raise Exception(result)

#         self.update_state(state="PLAN", meta={"done": "5 of 5"})
#         result = ProviderActions.plan(
#             name,
#             stack_name,
#             branch,
#             environment,
#             team,
#             version,
#             secreto,
#             variables_file,
#             project_path,
#         )
#         if result["rc"] != 0:
#             logger.error(
#                 f"Error when User {user} launch plan {name} with stack {stack_name} on team {team} and environment {environment} execute terraform plan"
#             )
#             raise Exception(result)
#         return result
#     except Exception as err:
#         self.retry(countdown=5, exc=err, max_retries=1)
#         self.update_state(state=states.FAILURE, meta={"exc": result})
#         raise Ignore()
#     finally:
#         dir_path = f"/tmp/{ stack_name }/{environment}/{team}/{name}"
#         Utils.delete_local_folder(dir_path)
#         r.delete(f"{name}-{team}-{environment}")


@celery_app.task(
    bind=True, acks_late=True, time_limit=30, name="pipeline git pull"
)
def pipeline_git_pull(
    self,
    git_repo: str,
    name: str,
    stack_name: str,
    environment: str,
    team: str,
    branch: str,
    project_path: str,
):
    try:
        git_result = ProviderRequirements.artifact_download(
            name, stack_name, environment, team, git_repo, branch, project_path
        )
        if git_result["rc"] != 0:
            raise Exception(git_result.get("stdout"))

        self.update_state(state="GET_VARS_AS_JSON", meta={"done": "2 of 2"})
        result = ProviderGetVars.json_vars(
            environment=environment,
            stack_name=stack_name,
            team=team,
            name=name,
            project_path=project_path,
        )
        if result["rc"] != 0:
            raise Exception(result.get("stdout"))
        result["tfvars"] = git_result["tfvars"]
        return result
    except Exception as err:
        self.retry(countdown=1, exc=err, max_retries=settings.TASK_MAX_RETRY)
        self.update_state(state=states.FAILURE, meta={"exc": result})
        raise Ignore()
    finally:
        dir_path = f"/tmp/{ stack_name }/{environment}/{team}/{name}"
        print(dir_path)


@celery_app.task(
    bind=True, acks_late=True, time_limit=30, name="pipeline copy template"
)
def pipeline_copy_template(
    self,
    name: str,
    stack_name: str,
    stack_type: str,
    csp_type: str,
    environment: str,
    team: str,
):
    try:
        copy_result = ProviderRequirements.artifact_copy(
            name=name,
            stack_name=stack_name,
            stack_type=stack_type,
            csp_type=csp_type,
            environment=environment,
            team=team
        )
        if copy_result["rc"] != 0:
            raise Exception(copy_result.get("stdout"))
    
        print(copy_result)

        self.update_state(state="GET_VARS_AS_JSON", meta={"done": "2 of 2"})
        result = ProviderGetVars.json_vars(
            environment=environment,
            stack_name=stack_name,
            stack_type=stack_type,
            csp_type=csp_type,
            team=team,
            name=name,
        )
        if result["rc"] != 0:
            raise Exception(result.get("stdout"))
        result["tfvars"] = copy_result["tfvars"]

        return result
    except Exception as err:
        self.retry(countdown=1, exc=err, max_retries=settings.TASK_MAX_RETRY)
        self.update_state(state=states.FAILURE, meta={"exc": result})
        raise Ignore()

@celery_app.task(
    bind=True, acks_late=True, time_limit=30, name="download git repo"
)
def git(
    self,
    git_repo: str,
    name: str,
    stack_name: str,
    environment: str,
    team: str,
    branch: str,
):
    try:
        result = ProviderRequirements.artifact_download(
            name, stack_name, environment, team, git_repo, branch
        )
    except Exception as err:
        self.retry(
            countdown=30, exc=err, max_retries=settings.TASK_MAX_RETRY
        )
        self.update_state(state=states.FAILURE, meta={"exc": result})
        raise Ignore()
    return stack_name, environment, team, name, result
