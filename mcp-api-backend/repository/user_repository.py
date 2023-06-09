import datetime
from unittest import result
from sqlalchemy.orm import Session
import db.model.user_model as models
from config.api_config import settings
from sqlalchemy import exc
import entity.user_entity as schemas
from src.shared.security.vault import get_password_hash

Usermodel = models.User


def create_user(db: Session, user: schemas.UserCreate):
    db_user = Usermodel(**user.dict())
    db_user.password = get_password_hash(user.password)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except exc.IntegrityError as err:
        raise ValueError(str(err.__dict__["orig"]))
    except Exception as err:
        raise err

def create_init_user(db: Session, password: str):
    db_user = models.User(
        username=settings.INIT_USER.get("username"),
        password=get_password_hash(password),  # TODO: password hashing 하는 것으로 바꿔야 함
        fullname=settings.INIT_USER.get("fullname"),
        email=settings.INIT_USER.get("email"),
        role=["system_manager"],
        team="team",
        is_active=True
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as err:
        raise err

def get_user_by_username(db: Session, username: str):
    try:
        return db.query(Usermodel).filter(Usermodel.username == username).first()
    except Exception as err:
        raise err

def get_user_by_id(db: Session, id: int):
    try:
        return db.query(Usermodel).filter(Usermodel.id == id).first()
    except Exception as err:
        raise err

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(Usermodel).offset(skip).limit(limit).all()
    except Exception as err:
        raise err

def get_users_by_team(db: Session, team: str, skip: int = 0, limit: int = 100):
    try:
        return db.query(Usermodel).filter(Usermodel.team == team).all()
    except Exception as err:
        raise err

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(Usermodel).filter(Usermodel.id == user_id).first()
    db_user.updated_at = datetime.datetime.now()
    check_None = [None, "", "string", []]
    if user.password not in check_None:
        db_user.password = get_password_hash(user.password)
    if user.username not in check_None:
        db_user.username = user.username
    if user.email not in check_None:
        db_user.email = user.email
    if user.fullname not in check_None:
        db_user.fullname = user.fullname
    if user.team not in check_None:
        db_user.team = user.team
    if user.role not in check_None:
        db_user.role = user.role
    if user.is_active not in check_None:
        db_user.is_active = user.is_active
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as err:
        raise err

def is_active(db: Session, user: schemas.UserCreate):
    try:
        return user.is_active
    except Exception as err:
        raise err

def is_superuser(db: Session, user: schemas.UserCreate) -> bool:
    try:
        super_role = {"team_manager", "system_manager"}
        return bool(set(user.role).intersection(super_role))
    except Exception as err:
        raise err

def is_master(db: Session, user: schemas.UserCreate) -> bool:
    try:
        master_role = ["system_manager"]
        return bool(set(user.role).intersection(master_role))
    except Exception as err:
        raise err

