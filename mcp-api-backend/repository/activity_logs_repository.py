import datetime

from sqlalchemy.orm import Session

from db.model import activity_log_model as models


def create_activity_log(db: Session, username: str, team: str, action: str):
    db_activity = models.ActivityLogs(
        username=username,
        team=team,
        created_at=datetime.datetime.now(),
        action=action,
    )
    try:
        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)
        return db_activity
    except Exception as err:
        raise err


def get_all_activity(db: Session, skip: int = 0, limit: int = 100):
    try:
        db_query = db.query(models.ActivityLogs)
        return (
            db_query.order_by(models.ActivityLogs.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    except Exception as err:
        raise err


def get_all_activity_by_team(db: Session, team: str, skip: int = 0, limit: int = 100):
    try:
        from sqlalchemy import func

        result = []
        for i in team:
            a = f'["{i}"]'
            result.extend(
                db.query(models.ActivityLogs)
                .filter(func.json_contains(models.ActivityLogs.team, a) == 1)
                .order_by(models.ActivityLogs.created_at.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
        return set(result)
    except Exception as err:
        raise err


def get_activity_by_username(db: Session, username: int):
    try:
        return (
            db.query(models.ActivityLogs)
            .filter(models.ActivityLogs.username == username)
            .all()
        )
    except Exception as err:
        raise err


def get_activity_by_username_team(db: Session, username: int, team: str):
    try:
        return (
            db.query(models.ActivityLogs)
            .filter(models.ActivityLogs.username == username)
            .filter(models.ActivityLogs.team == team)
            .all()
        )
    except Exception as err:
        raise err
