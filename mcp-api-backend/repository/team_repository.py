import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import db.model.team_model as models
from config.api_config import settings
from sqlalchemy import exc
import entity.team_entity as schemas


def create_team(db: Session, team_name: str):
    db_team = models.Team(team_name=team_name)
    try:
        db.add(db_team)
        db.commit()
        db.refresh(db_team)
        return db_team
    except IntegrityError as err:
        raise HTTPException(
            status_code=409, detail=str(err.__dict__["orig"])
        )
    except Exception as err:
        raise err


def get_team_by_name(db: Session, team_name: str):
    try:
        return (
            db.query(models.Team)
            .filter(models.Team.team_name == team_name).first()
        )
    except Exception as err:
        raise err
