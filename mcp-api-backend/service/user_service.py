from repository import user_repository
from sqlalchemy.orm import Session
from utils.utils import object_as_dict


def get_admin_info(db: Session):
    user = user_repository.get_user_by_username(db, "admin")
    return object_as_dict(user)
