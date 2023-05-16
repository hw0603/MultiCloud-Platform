from sqlalchemy.orm import Session
import db.model.user_model as models
from config.api_config import settings
from sqlalchemy import exc
import entity.user_entity as schemas
from src.shared.security.vault import get_password_hash

Usermodel = models.User


def get_user_by_username(db: Session, username: str):
    try:
        return db.query(Usermodel).filter(Usermodel.username == username).first()
    except Exception as err:
        raise err

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
        password=password,  # TODO: password hashing 하는 것으로 바꿔야 함
        fullname=settings.INIT_USER.get("fullname"),
        email=settings.INIT_USER.get("email"),
        role="{System_Manager : True}",
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

def is_superuser(db: Session, user: schemas.UserCreate) -> bool:
    ...  # TODO: 구현하기
    return True

def is_master(db: Session, user: schemas.UserCreate) -> bool:
    ...  # TODO: 구현하기
    return True

