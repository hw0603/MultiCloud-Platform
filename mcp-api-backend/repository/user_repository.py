from sqlalchemy.orm import Session
import db.model.user_model as models
import entity.user_entity as schemas

Usermodel = models.User

def get_user_by_username(db: Session, username: str):
    try:
        return db.query(Usermodel).filter(Usermodel.username == username).first()
    except Exception as err:
        raise err

def is_superuser(db: Session, user: schemas.UserCreate) -> bool:
    ...  # TODO: 구현하기
    return True

def is_master(db: Session, user: schemas.UserCreate) -> bool:
    ...  # TODO: 구현하기
    return True
