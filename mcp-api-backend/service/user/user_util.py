from dependency_injector.wiring import Provide, inject
from service.user.user_validator import Container
from fastapi import Depends, HTTPException, status


@inject
def validate_password(
    username: str, password: str, user_validate_service=Provide[Container.user_validate_service]
):
    (result, additional_info) = user_validate_service.validate(username, password)
    print((result, additional_info))
    if not result:
        raise HTTPException(
            status_code=400,
            detail=f"{additional_info}",
        )
    return True


container = Container()
container.wire(modules=[__name__])
