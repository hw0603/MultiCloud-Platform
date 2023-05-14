from password_strength import PasswordPolicy

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
    

    