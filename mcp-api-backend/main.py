from src.shared.security import deps
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from src.users.infrastructure import repositories


app = FastAPI()

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

@app.get("/")
def get_userinfo_from_db(db: Session = Depends(deps.get_db)):
    user = repositories.get_user_by_username(db, "admin")
    return object_as_dict(user)
