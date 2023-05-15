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
    

