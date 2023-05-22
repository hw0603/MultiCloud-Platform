from multiprocessing import connection
from fastapi import HTTPException, Depends

from entity.user_entity import UserUpdate
from config.api_config import settings
from repository import user_repository as crud_users
from sqlalchemy.orm import Session
from db.connection import get_db
from utils.utils import object_as_dict
from utils.user_utils import check_team_user, check_role_user, validate_email
from entity.user_entity import UserInit, UserCreate, User
from utils.user_utils import validate_password
from src.shared.security import deps

def get_admin_info(db: Session):
    user = crud_users.get_user_by_username(db, "admin")
    return object_as_dict(user)


async def create_init_user(passwd: UserInit, db: Session = Depends(get_db)):
    init_user = settings.INIT_USER
    validate_password(init_user.get("username"), passwd.password)
    db_user = crud_users.get_user_by_username(db, username=init_user.get("username"))
    if db_user:
        raise HTTPException(status_code=409, detail="이미 등록된 username입니다.")
    else:
        try:
            return crud_users.create_init_user(db=db, password=passwd.password)
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))

async def create_user(
        user: UserCreate, 
        current_user: User = Depends(deps.get_current_active_user),
        db: Session = Depends(get_db)
):
    # 요청한 사용자가 지원하는 role을 갖고있는지 확인
    roles = ["system_manager", "team_manager", "user"]
    if not all(item in roles for item in user.role):
        raise HTTPException(
            status_code=403,
            detail=f"지원하지 않는 권한이 존재합니다. 지원하는 권한은 {settings.ALL_ROLE}입니다."
        )
    # team_manager가 아니면 user를 생성할 수 없음
    if not crud_users.is_superuser(db, current_user):
        raise HTTPException(status_code=403, detail="해당 작업에 대한 권한이 없습니다.")
    # team_manager일 때는 생성할 user와 팀이 같은지 확인 (자신의 팀 내의 사용자만 추가할 수 있으므로)
    if not crud_users.is_master(db, current_user):
        if not check_team_user(current_user.team, user.team):
            raise HTTPException(
                status_code=403,
                detail=f"{user.team}에 사용자를 추가할 권한이 없습니다."
            )
        # team_manager는 user 권한을 가진 사용자만 추가 가능
        if not check_role_user(user.role):
            raise HTTPException(
                status_code=403,
                detail=f"{user.role} 권한을 가진 사용자를 추가할 권한이 없습니다."
            )
    # 추가하려는 사용자가 이미 존재하는지 확인
    db_user = crud_users.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="이미 등록된 username입니다")
    
    validate_password(user.username, user.password)
    try:
        result = crud_users.create_user(db=db, user=user)
        # TODO: logging 추가
        return result
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

async def get_user_list(
        current_user: User = Depends(deps.get_current_active_user),
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    # 일반 user는 사용자 목록을 조회할 수 없음
    if not crud_users.is_superuser(db, current_user):  
        raise HTTPException(status_code=403, detail="해당 작업에 대한 권한이 없습니다.")
    try:
        # team_manager는 자신이 속한 team의 사용자 목록만 조회가능
        if not crud_users.is_master(db, current_user):
            return crud_users.get_users_by_team(
                db=db, team=current_user.team, skip=skip, limit=limit
            )
        # system_manager는 모든 사용자 목록 조회가능
        return crud_users.get_all_users(db=db, skip=skip, limit=limit)  # master(system_manager)는 모든 user 조회
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))
    
async def get_user_by_id_or_name(
        user,
        current_user: User = Depends(deps.get_current_active_user),
        db: Session = Depends(get_db),
):
    if not crud_users.is_superuser(db, current_user):
        raise HTTPException(status_code=403, detail="해당 작업에 대한 권한이 없습니다.")
    try:
        if not user.isdigit():
            user_info = crud_users.get_user_by_username(db=db, username=user)
        else:
            user_info = crud_users.get_user_by_id(db=db, id=user)
        if user_info == None:
            raise ValueError(f"사용자 {user}는 존재하지 않습니다.")
        # team_manager는 조회하고자 하는 사용자와 팀이 같은 사용자만 조회 가능
        if not crud_users.is_master(db, current_user):
            if not check_team_user(current_user.team, user_info.team):
                raise Exception("해당 작업에 대한 권한이 없습니다.")
        return user_info
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

async def update_user(
        user_id: str,
        user: UserUpdate,
        current_user: User = Depends(deps.get_current_active_user),
        db: Session = Depends(get_db)
):
    # 일반 user는 사용자 정보를 수정할 수 없음
    if not crud_users.is_superuser(db, current_user):
        raise HTTPException(status_code=403, detail="해당 작업에 대한 권한이 없습니다.")
    # 요청한 사용자가 지원하는 role을 갖고있는지 확인
    roles = ["system_manager", "team_manager", "user"]
    if not all(item in roles for item in user.role):
        raise HTTPException(
            status_code=403,
            detail="지원하지 않는 권한이 존재합니다. 지원하는 권한은 system_manager, team_manager, user입니다."
        )
    existing_user = crud_users.get_user_by_id(db, user_id)
    # team_manager 권한을 가진 사용자에 대한 검증
    if not crud_users.is_master(db, current_user):
        # team_manager는 같은 팀에 속한 사용자만 수정 가능
        if not check_team_user(current_user.team, existing_user.team):
            raise HTTPException(
                status_code=403,
                detail=f"팀 {existing_user.team}의 사용자를 수정할 권한이 없습니다."
            )
        # team_manager는 user 권한을 가진 사용자만 수정 가능
        if not check_role_user(existing_user.role):
            raise HTTPException(
                status_code=403,
                detail=f"{existing_user.role} 권한을 가진 사용자를 수정할 권한이 없습니다."
            )
    check_None = [None, "", "string"]
    if user.password not in check_None:
        validate_password(user.username, user.password)
    if user.email not in check_None:
        validate_email(user.email)
    try:
        result = crud_users.update_user(db=db, user_id=user_id, user=user)
        print(user.role)
        # TODO: logging 추가
        return result
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))
