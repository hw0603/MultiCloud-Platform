from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from service import instance_service, grafana_service
from typing import Optional, List
from api.api_response import *
from db.connection import get_db, get_async_db
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session,
)
from config.api_config import settings as api_settings  # for testing
import logging

from entity import stack_entity as schemas_stacks
from entity import user_entity as schemas_users

router = APIRouter()
logger = logging.getLogger("uvicorn")


from fastapi import APIRouter, Depends

from service import stack_service

router = APIRouter()


@router.post("/", response_model=schemas_stacks.Stack)
async def create_new_stack(
    create_stack: schemas_stacks.StackCreate = Depends(stack_service.create_new_stack),
):
    return create_stack


# @router.patch("/{stack_id}", response_model=schemas_stacks.Stack)
# async def update_stack(
#     update_stack: schemas_stacks.StackCreate = Depends(stack_service.update_stack),
# ):
#     return update_stack


@router.get("/")
async def get_all_stacks(
    get_all_stacks: schemas_stacks.Stack = Depends(stack_service.get_all_stacks),
):
    return get_all_stacks


@router.get("/{stack}")
async def get_stack_by_id_or_name(
    get_stack: schemas_stacks.Stack = Depends(stack_service.get_stack_by_id_or_name),
):
    return get_stack


@router.delete("/{stack}")
async def delete_stack_by_id_or_name(
    delete_stack: schemas_stacks.Stack = Depends(stack_service.delete_stack_by_id_or_name),
):
    return delete_stack
