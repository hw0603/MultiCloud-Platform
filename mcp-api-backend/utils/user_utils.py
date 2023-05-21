from http import HTTPStatus
from dependency_injector.wiring import Provide, inject
from email_validator import EmailNotValidError
from fastapi import Depends, HTTPException, status

from typing import Tuple
import re
from dependency_injector import containers, providers
from password_strength import PasswordPolicy
from usernames import is_safe_username

class PasswordValidator:
    def __init__(self) -> None:
        self._policy = PasswordPolicy.from_names(
            length=8 # , uppercase=1, numbers=1, special=1, nonletters=1  ! 비밀번호 정책 임시로 완화
        )
    
    def validate(self, password: str) -> bool:
        if password is None or len(password) == 0:
            return False
        if len(self._policy.test(password)) > 0: # 실패한 테스트의 목록을 반환받음 / 길이가 0 -> 성공, 0보다 크면 -> 실패
            return False
        return True
    

class UsernameValidator:
    def __init__(self) -> None:
        self._whitelist = ['admin']                            # 항상 safe한 것으로 간주되는 단어 목록
        self._black_list = ["guest", "root", "administrator"]  # unsafe한 것으로 간주되어야 하는 단어 목록
        self._max_length = 12                                  # 최대 길이

    def validate(self, username: str) -> bool:
        return is_safe_username(
            username,
            whitelist=self._whitelist,
            blacklist=self._black_list,
            max_length = self._max_length,
        )

class EmailValidator:
    def __init__(self) -> None:
        self.regex_email = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    
    def validate(self, email: str):
        if not re.fullmatch(self.regex_email, email):
            return False
        return True
        
class UserValidator:
    def __init__(
            self,
            username_validator: UsernameValidator,
            password_validator: PasswordValidator,
    ):
        self.username_validator = username_validator
        self.password_validator = password_validator

    def validate(self, username: str, password: str) -> Tuple[str, str]:
        if not self.password_validator.validate(password):
            return (False, "Password weak")
        elif not self.username_validator.validate(username):
            return (False, "Username invalid")
        return (True, "")


class Container(containers.DeclarativeContainer):
    username_validator = providers.Singleton(UsernameValidator)
    password_validator = providers.Singleton(PasswordValidator)
    email_validator = providers.Singleton(EmailValidator)

    user_validate_service = providers.Singleton(
        UserValidator, username_validator, password_validator
    )

@inject
def validate_password(
    username: str, password: str, user_validate_service=Provide[Container.user_validate_service]
):
    (result, additional_info) = user_validate_service.validate(username, password)
    if not result:
        raise HTTPException(
            status_code=400,
            detail=f"{additional_info}",
        )
    return True

@inject
def validate_email(
    email: str, email_validate_service=Provide[Container.email_validator]
):
    if not email_validate_service.validate(email):
        raise HTTPException(
            status_code=400,
            detail="올바르지 않은 email 주소입니다."
        )
    return True

container = Container()
container.wire(modules=[__name__])

def check_team_user(owner_team: str, add_user_team: str) -> bool:
    return owner_team == add_user_team

def check_role_user(add_user_role: str):
    return add_user_role == ["user"]