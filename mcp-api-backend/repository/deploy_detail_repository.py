import datetime

from sqlalchemy.orm import Session

import entity.deploy_detail_entity as schemas_deploy
import db.model.deploy_detail_model as models


def create_new_deploy_detail(
    db: Session,
    deploy_id: int,
    stack_id: int,
    deploy_detail: schemas_deploy.DeployDetailCreate,
):
    db_deploy_detail = models.DeployDetail(
        deploy_id=deploy_id,
        stack_id=stack_id,
        tfvar_file=deploy_detail.tfvar_file,
        variables=deploy_detail.variables,
    )
    try:
        db.add(db_deploy_detail)
        db.commit()
        db.refresh(db_deploy_detail)
        return db_deploy_detail
    except Exception as err:
        raise err
