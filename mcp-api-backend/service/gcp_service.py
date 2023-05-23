from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session

import repository.activity_logs_repository as crud_activity
import repository.user_repository as crud_user
import repository.gcp_repository as crud_gcp
import entity.gcp_entity as schemas_gcp
import entity.user_entity as schemas_user
from src.shared.security import deps


async def new_gcloud_profile(
    gcp: schemas_gcp.GcloudBase,
    response: Response,
    current_user: schemas_user.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    # 사용자에게 권한이 있는지 확인
    if not crud_user.is_master(db, current_user):
        raise HTTPException(
            status_code=403, 
            detail="해당 사용자에게 권한이 없습니다."
        )
    
    if "string" in [gcp.team, gcp.environment]:
        raise HTTPException(
            status_code=409,
            detail="팀 혹은 환경설정의 입력이 잘못 되었습니다. 다시 한 번 확인해주세요."
        )
    
    db_gcp_account = crud_gcp.get_team_gcloud_profile(
        db=db, team=gcp.team, environment=gcp.environment
    )
    
    if db_gcp_account:
        raise HTTPException(
            status_code=409, 
            detail="이미 존재하는 계정입니다."
        )
    
    try:
        result = crud_gcp.create_gcloud_profile(
            db=db,
            team=gcp.team,
            environment=gcp.environment,
            gcloud_keyfile_json=gcp.gcloud_keyfile_json,
        )
        crud_activity.create_activity_log(
            db=db,
            username=current_user.username,
            team=current_user.team,
            action=f"Create GCP account {result.id}",
        )
        return {"result": f"Create GCP account {gcp.team} {gcp.environment}"}
    
    except Exception as err:
        raise HTTPException(status_code=400, detail=err)
    

async def all_gcloud_accounts(
    current_user: schemas_user.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    if not crud_user.is_master(db, current_user):
        return crud_gcp.get_team_gcloud_profile(
            db=db, team=current_user.team, environment=None
        )
    return crud_gcp.get_all_gcloud_profile(db=db)


async def gcloud_account_by_id(
    gcloud_account_id,
    current_user: schemas_user.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    if not crud_user.is_master(db, current_user):
        raise HTTPException(
            status_code=400, 
            detail="해당 사용자에게 권한이 없습니다."
        )
    
    result = crud_gcp.delete_gcloud_profile_by_id(
        db=db, gcloud_profile_id=gcloud_account_id
    )
    crud_activity.create_activity_log(
        db=db,
        username=current_user.username,
        team=current_user.team,
        action=f"Delete GCP account {gcloud_account_id} team",
    )
    return result

