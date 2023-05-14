from typing import Tuple

from dependency_injector import containers, providers
from password_strength import PasswordPolicy
from usernames import is_safe_username

class PasswordValidator:
    def __init__(self) -> None:
        self._policy = PasswordPolicy.from_names(
            length=8, uppercase=1, numbers=1, special=1, nonletters=1
        )
    
    def validate(self, password: str) -> bool:
        if password == None or len(password) == 0:
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


class Container(containers.DeclarativeContainer):
    username_validator = providers.Singleton(UsernameValidator)
    password_validator = providers.Singleton(PasswordValidator)

    user_validate_service = providers.Singleton(
        UserValidator, username_validator, password_validator
    )