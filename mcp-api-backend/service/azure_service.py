from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session

import repository.activity_logs_repository as crud_activity
import repository.user_repository as crud_user
import repository.azure_repository as crud_azure
import entity.azure_entity as schemas_azure
import entity.user_entity as schemas_user
from src.shared.security import deps


async def create_new_azure_profile(
    azure: schemas_azure.AzureBase,
    current_user: schemas_user.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    if not crud_user.is_master(db, current_user):
        raise HTTPException(
            status_code=403, 
            detail="해당 사용자에게 권한이 없습니다."
        )
    
    if "string" in [azure.team, azure.environment]:
        raise HTTPException(
            status_code=409,
            detail="팀 혹은 환경설정의 입력이 잘못 되었습니다. 다시 한 번 확인해주세요."
        )
    
    db_azure_account = crud_azure.get_team_azure_profile(
        db=db, team=azure.team, environment=azure.environment
    )

    if db_azure_account:
        raise HTTPException(
            status_code=409, 
            detail="이미 존재하는 계정입니다."
        )
    
    try:
        result = crud_azure.create_azure_profile(db=db, azure=azure)
        crud_activity.create_activity_log(
            db=db,
            username=current_user.username,
            team=current_user.team,
            action=f"Create Azure Account {azure.subscription_id}",
        )
        return result
    
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=str(err)
        )


async def get_all_azure_accounts(
        current_user: schemas_user.User = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
):
    if not crud_user.is_master(db, current_user):
        return crud_azure.get_team_azure_profile(
            db=db, team=current_user.team, environment=None
        )
    
    return crud_azure.get_all_azure_profile(db=db)


async def azure_account_by_id(
        azure_account_id: int,
        current_user: schemas_user = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
):
    if not crud_user.is_master(db, current_user):
        raise HTTPException(
            status_code=403,
            detail="해당 사용자에게 권한이 없습니다."
        )
    
    result = crud_azure.delete_azure_profile_by_id(
        db=db, azure_profile_id=azure_account_id
    )
    crud_activity.create_activity_log(
        db=db,
        username=current_user.username,
        squad=current_user.squad,
        action=f"Delete Azure account {azure_account_id}",
    )

    return result
