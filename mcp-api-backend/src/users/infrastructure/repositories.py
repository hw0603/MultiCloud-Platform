from sqlalchemy.orm import Session
import src.users.infrastructure.models as models


def get_user_by_username(db: Session, username: str):
    try:
        return db.query(models.User).filter(models.User.username == username).first()
    except Exception as err:
        raise err
