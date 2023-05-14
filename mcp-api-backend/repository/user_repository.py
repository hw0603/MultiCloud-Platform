from sqlalchemy.orm import Session
import db.model.user_model as models
from config.user_config import settings

Usermodel = models.User


def get_user_by_username(db: Session, username: str):
    try:
        return db.query(Usermodel).filter(Usermodel.username == username).first()
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
        print(db_user.team)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as err:
        raise err
