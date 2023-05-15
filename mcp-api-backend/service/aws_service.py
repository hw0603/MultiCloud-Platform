from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import repository.activity_logs_repository as crud_activity
import repository.user_repository as crud_user
import entity.aws_entity as schemas_aws
import entity.user_entity as schemas_user


async def create_new_aws_profile(
        
)