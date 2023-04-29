from sqlalchemy.orm import Session
import db.model.user_model as models

Usermodel = models.User

def get_user_by_username(db: Session, username: str):
    try:
        return db.query(Usermodel).filter(Usermodel.username == username).first()
    except Exception as err:
        raise err
