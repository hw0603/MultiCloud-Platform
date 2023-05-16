from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import repository.activity_logs_repository as crud_activity
import repository.user_repository as crud_user
import repository.aws_repository as crud_aws
import entity.aws_entity as schemas_aws
import entity.user_entity as schemas_user
from src.shared.security import deps


async def create_new_aws_profile(
    aws: schemas_aws.AwsAsumeProfile,
    current_user: schemas_user.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    # 사용자에게 권한이 있는지 확인
    if not crud_user.is_master(db, current_user):
        raise HTTPException(
            status_code=403, 
            detail="해당 사용자에게 권한이 없습니다."
        )
    
    if "string" in [aws.team, aws.environment]:
        raise HTTPException(
            status_code=409,
            detail="팀 혹은 환경설정의 입력이 잘못 되었습니다. 다시 한 번 확인해주세요."
        )
    
    db_aws_account = crud_aws.get_team_aws_profile(
        db=db, team=aws.team, environment=aws.environment
    )

    if db_aws_account:
        raise HTTPException(
            status_code=409, 
            detail="이미 존재하는 계정입니다.")
    
    try:
        result = crud_aws.create_aws_profile(db=db, aws=aws)
        crud_activity.create_activity_log(
            db=db,
            username=current_user.username,
            team=current_user.team,
            action=f"Create AWS account {aws.team} {aws.environment}",
        )
        return {"result": f"Create AWS account {aws.team} {aws.environment}"}
    
    except Exception as err:
        raise HTTPException(
            status_code=400, 
            detail=str(err)
        )
    

async def get_all_aws_accounts(
        current_user: schemas_user.User = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
):
    # 사용자에게 권한이 있는지 확인
    if not crud_user.is_master(db, current_user):
        return crud_aws.get_team_aws_profile(
            db=db, team=current_user.team, environment=None
        )
    return crud_aws.get_all_aws_profile(db=db)

