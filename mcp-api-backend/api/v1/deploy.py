from fastapi import APIRouter, Depends

from entity import deploy_detail_entity as schemas_deploy
from service import deploy_service

router = APIRouter()


@router.post("/", status_code=202)
async def deploy_infra_by_stack_name(
    create_deploy: schemas_deploy.DeployDetailCreate = Depends(
        deploy_service.deploy_infra_by_stack_name
    ),
):
    return create_deploy


# @router.patch("/{deploy_id}", status_code=202)
# async def update_deploy_by_id(
#     update_deploy: schemas_deploy.DeployDetailUpdate = Depends(deploy_service.deploy_by_id),
# ):
#     return update_deploy


# @router.put("/{deploy_id}", status_code=202)
# async def destroy_infra(
#     destroy_deploy: schemas_deploy.DeployBase = Depends(deploy_service.destroy_infra),
# ):
#     return destroy_deploy


# @router.delete("/{deploy_id}")
# async def delete_infra_by_id(
#     delete_deploy: schemas_deploy.DeployBase = Depends(deploy_service.delete_infra_by_id),
# ):
#     return delete_deploy


# @router.get("/")
# async def get_all_deploys(
#     get_all_deploys: schemas_deploy.DeployBase = Depends(deploy_service.get_all_deploys),
# ):
#     return get_all_deploys


# @router.get("/{deploy_id}")
# async def get_deploy_by_id(
#     get_deploy: schemas_deploy.DeployBase = Depends(deploy_service.get_deploy_by_id),
# ):
#     return get_deploy


# @router.get("/output/{deploy_id}", status_code=200)
# async def get_output(
#     get_output: schemas_deploy.DeployBase = Depends(deploy_service.get_output),
# ):
#     return get_output


# @router.put("/unlock/{deploy_id}", status_code=200)
# async def unlock_deploy(
#     unlock_deploy: schemas_deploy.DeployBase = Depends(deploy_service.unlock_deploy),
# ):
#     return unlock_deploy


# @router.get("/show/{deploy_id}", status_code=202)
# async def get_show(
#     get_show: schemas_deploy.DeployBase = Depends(deploy_service.get_show),
# ):
#     return get_show
