from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session

import repository.activity_logs_repository as crud_activity
import repository.user_repository as crud_user
import repository.custom_provider_repository as crud_custom_provider
import entity.custom_provider_entity as schemas_custom_provider
import entity.user_entity as schemas_user
from src.shared.security import deps


async def create_custom_provider_profile(
    custom_provider: schemas_custom_provider.CustomProviderBase,
    response: Response,
    current_user: schemas_user.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    if not crud_user.is_master(db, current_user):
        raise HTTPException(
            status_code=403,
            detail="해당 사용자에게 권한이 없습니다."
        )
    
    if "string" in [custom_provider.team, custom_provider.environment]:
        raise HTTPException(
            status_code=409,
            detail="팀 혹은 환경설정의 입력이 잘못 되었습니다. 다시 한 번 확인해주세요."
        )
    
    db_custom_provider_account = crud_custom_provider.get_team_custom_provider_profile(
        db=db, team=custom_provider.team, environment=custom_provider.environment
    )

    if db_custom_provider_account:
        raise HTTPException(
            status_code=409,
            detail="이미 존재하는 계정입니다."
        )
    
    try:
        result = crud_custom_provider.create_custom_provider_profile(
            db=db,
            team=custom_provider.team,
            environment=custom_provider.environment,
            configuration_keyfile_json=custom_provider.configuration,
        )

        crud_activity.create_activity_log(
            db=db,
            username=current_user.username,
            team=current_user.team,
            action=f"커스텀 프로바이더 생성 ({result.id})",
        )

        return {"result": f"Create custom provider account {custom_provider.team} {custom_provider.environment}"}
    
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=err
        )


async def all_custom_providers_accounts(
    current_user: schemas_user.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    if not crud_user.is_master(db, current_user):
        return crud_custom_provider.get_team_custom_provider_profile(
            db=db, team=current_user.team, environment=None 
        )

    return crud_custom_provider.get_all_custom_profile(db=db)


async def custom_provider_account_by_id(
    custom_provider_id,
    current_user: schemas_user.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    if not crud_user.is_master(db, current_user):
        raise HTTPException(
            status_code=400,
            detail="해당 사용자에게 권한이 없습니다."
        )
    
    result = crud_custom_provider.delete_custom_profile_by_id(
        db=db, custom_profile_id=custom_provider_id
    )

    crud_activity.create_activity_log(
        db=db,
        username=current_user.username,
        team=current_user.team,
        action=f"커스텀 프로바이더 삭제. ({custom_provider_id})",
    )
    
    return result

