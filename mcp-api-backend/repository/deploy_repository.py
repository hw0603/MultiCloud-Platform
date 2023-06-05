import datetime

from sqlalchemy.orm import Session

import entity.deploy_entity as schemas_deploy
import db.model.deploy_model as models


def create_new_deploy(
    db: Session,
    deploy: schemas_deploy.DeployCreate,
    user_id: int,
    team: str,
    task_id: str,
    username: str,
):
    db_deploy = models.Deploy(
        deploy_name=deploy.deploy_name,
        start_time=deploy.start_time,
        destroy_time=deploy.destroy_time,
        user_id=user_id,
        username=username,
        team=team,
        environment=deploy.environment,
        created_at=datetime.datetime.now(),
        detail_cnt=len(deploy.deploy_detail),
        task_id=task_id,
    )
    try:
        db.add(db_deploy)
        db.commit()
        db.refresh(db_deploy)
        return db_deploy
    except Exception as err:
        raise err

# def update_deploy_cnt(
#         db: Session,
#         deploy_id: int
# ):
#     db_deploy = db.query(models.Deploy).filter(models.Deploy.deploy_id == deploy_id).first()
#     db_deploy.detail_cnt -= 1
#     try:
#         db.add(db_deploy)
#         db.commit()
#         db.refresh(db_deploy)
#         return db_deploy
#     except Exception as err:
#         raise err

# def update_deploy(
#     db: Session,
#     deploy_id: int,
#     action: str,
#     username: str,
#     user_id: int,
#     task_id: str,
#     start_time: str,
#     destroy_time: str,
#     stack_branch: str,
#     tfvar_file: str,
#     project_path: str,
#     variables: dict,
# ):
#     db_deploy = db.query(models.Deploy).filter(models.Deploy.id == deploy_id).first()

#     db_deploy.action = action
#     db_deploy.task_id = task_id
#     db_deploy.username = username
#     db_deploy.user_id = user_id
#     db_deploy.stack_branch = stack_branch
#     db_deploy.tfvar_file = tfvar_file
#     db_deploy.project_path = project_path
#     db_deploy.variables = variables
#     db_deploy.updated_at = datetime.datetime.now()
#     check_None = ["string"]
#     if db_deploy.start_time not in check_None:
#         db_deploy.start_time = start_time
#     if db_deploy.destroy_time not in check_None:
#         db_deploy.destroy_time = destroy_time
#     try:
#         db.add(db_deploy)
#         db.commit()
#         db.refresh(db_deploy)
#         return db_deploy
#     except Exception as err:
#         raise err


# def update_plan(db: Session, deploy_id: int, action: str, task_id: str):

#     db_deploy = db.query(models.Deploy).filter(models.Deploy.id == deploy_id).first()

#     db_deploy.action = action
#     db_deploy.task_id = task_id
#     try:
#         db.add(db_deploy)
#         db.commit()
#         db.refresh(db_deploy)
#         return db_deploy
#     except Exception as err:
#         raise err


# def update_schedule(db: Session, deploy_id: int, start_time: str, destroy_time: str):

#     db_deploy = db.query(models.Deploy).filter(models.Deploy.id == deploy_id).first()

#     db_deploy.start_time = start_time
#     db_deploy.destroy_time = destroy_time
#     try:
#         db.add(db_deploy)
#         db.commit()
#         db.refresh(db_deploy)
#         return db_deploy
#     except Exception as err:
#         raise err


# def delete_deploy_by_id(db: Session, deploy_id: int, team: str):
#     db.query(models.Deploy).filter(models.Deploy.deploy_id == deploy_id).filter(
#         models.Deploy.team == team
#     ).delete()
#     try:
#         db.commit()
#         return {models.Deploy.deploy_id: "deleted", "Deploy_id": deploy_id}
#     except Exception as err:
#         raise err


def get_deploy_by_id(db: Session, deploy_id: int):
    try:
        return db.query(models.Deploy).filter(models.Deploy.deploy_id == deploy_id).first()
    except Exception as err:
        raise err


# def get_deploy_by_name(db: Session, deploy_name: str):
#     try:
#         return db.query(models.Deploy).filter(models.Deploy.name == deploy_name).first()
#     except Exception as err:
#         raise err


# def get_deploy_by_stack(db: Session, stack_name: str):
#     try:
#         return (
#             db.query(models.Deploy)
#             .filter(models.Deploy.stack_name == stack_name)
#             .first()
#         )
#     except Exception as err:
#         raise err


def get_deploy_by_id_team(db: Session, deploy_id: int, team: str):
    try:
        return (
            db.query(models.Deploy)
            .filter(models.Deploy.id == deploy_id)
            .filter(models.Deploy.team == team)
            .first()
        )
    except Exception as err:
        raise err


def get_deploy_by_name_team(
    db: Session, deploy_name: str, team: str, environment: str
):
    try:
        return (
            db.query(models.Deploy)
            .filter(models.Deploy.deploy_name == deploy_name)
            .filter(models.Deploy.team == team)
            .filter(models.Deploy.environment == environment)
            .first()
        )
    except Exception as err:
        raise err

def get_deploy_by_team(db: Session, team: str):
    try:
        return db.query(models.Deploy).filter(models.Deploy.team == team).all()
    except Exception as err:
        raise err

def get_all_deploys(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(models.Deploy).offset(skip).limit(limit).all()
    except Exception as err:
        raise err


# def get_all_deploys_by_team(db: Session, team: str, skip: int = 0, limit: int = 100):
#     try:
#         result = []
#         for i in team:
#             result.extend(
#                 db.query(models.Deploy).filter(models.Deploy.team == i).all()
#             )
#         return set(result)
#     except Exception as err:
#         raise err


# def get_deploy_by_cloud_account(db: Session, team: str, environment: str):
#     try:
#         return (
#             db.query(models.Deploy)
#             .filter(models.Deploy.environment == environment)
#             .filter(models.Deploy.team == team)
#             .first()
#         )
#     except Exception as err:
#         raise err
