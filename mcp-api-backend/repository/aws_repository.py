import datetime

from sqlalchemy.orm import Session
import db.model.aws_model as models
import entity.aws_entity as schemas_aws
from src.shared.security.vault import vault_encrypt, vault_decrypt


@vault_encrypt
def encrypt(secreto):
    try:
        return secreto
    except Exception as err:
        raise err


@vault_decrypt
def decrypt(secreto):
    try:
        return secreto
    except Exception as err:
        raise err


def create_aws_profile(db: Session, aws: schemas_aws.AwsAsumeProfile):
    encrypt_access_key_id = encrypt(aws.access_key_id)
    encrypt_secret_access_key = encrypt(aws.secret_access_key)
    db_aws = models.Aws_provider(
        access_key_id=encrypt_access_key_id,
        secret_access_key=encrypt_secret_access_key,
        default_region=aws.default_region,
        environment=aws.environment,
        profile_name=aws.profile_name,
        role_arn=aws.role_arn,
        source_profile=aws.source_profile,
        created_at=datetime.datetime.now(),
        team=aws.team,

    )
    check_None = [None, "string"]
    if db_aws.role_arn in check_None:
        db_aws.role_arn = ""
    if db_aws.profile_name in check_None:
        db_aws.profile_name = ""
    if db_aws.source_profile in check_None:
        db_aws.source_profile = ""
    try:
        db.add(db_aws)
        db.commit()     # 모든 작업의 정상 처리를 확정하는 명령어, 버퍼에 올라왔던 사항들을 모두 DB에 반영
        db.refresh(db_aws) # DB에서 최신 상태의 객체를 불러오는 명령어
        return db_aws
    except Exception as err:
        raise err
    

def get_credentials_aws_profile(db: Session, environment: str, team: str):
    get_access_key = (
        db.query(models.Aws_provider.access_key_id)
        .filter(models.Aws_provider.environment == environment)
        .filter(models.Aws_provider.team == team)
        .first()
    )
    get_secret_access_key = (
        db.query(models.Aws_provider.secret_access_key)
        .filter(models.Aws_provider.environment == environment)
        .filter(models.Aws_provider.team == team)
        .first()
    )
    default_region = (
        db.query(models.Aws_provider.default_region)
        .filter(models.Aws_provider.environment == environment)
        .filter(models.Aws_provider.team == team)
        .first()
    )
    profile_name = (
        db.query(models.Aws_provider.profile_name)
        .filter(models.Aws_provider.environment == environment)
        .filter(models.Aws_provider.team == team)
        .first()
    )
    role_arn = (
        db.query(models.Aws_provider.role_arn)
        .filter(models.Aws_provider.environment == environment)
        .filter(models.Aws_provider.team == team)
        .first()
    )
    source_profile = (
        db.query(models.Aws_provider.source_profile)
        .filter(models.Aws_provider.environment == environment)
        .filter(models.Aws_provider.team == team)
    )
    try:
        return {
            "access_key": decrypt(get_access_key[0]),
            "secret_access_key": decrypt(get_secret_access_key[0]),
            "default_region": default_region[0],
            "profile_name": profile_name[0],
            "role_arn": role_arn[0],
            "source_profile": source_profile[0],
        }
    except Exception as err:
        raise err 


def get_team_aws_profile(db: Session, team: str, environment: str):
    try:
        if environment != None:
            return (
                db.query(models.Aws_provider)
                .filter(models.Aws_provider.team == team)
                .filter(models.Aws_provider.environment == environment)
                .first()
            )
        result = []
        for i in team:
            result.extend(
                db.query(models.Aws_provider)
                .filter(models.Aws_provider.team == i)
                .all()
            )
        return set(result)
    except Exception as err:
        raise err 
    
