from abc import *

# 다양한 Storage를 지원하기 위한 추상화 클래스
class StorageBase(metaclass=ABCMeta):

    @abstractmethod
    def get(self, id: str):
        pass

    @abstractmethod
    def put(self, id: str, info: dict):
        pass

    @abstractmethod
    def lock(self, id: str, info: dict):
        pass

    @abstractmethod
    def unlock(self, id: str, info: dict):
        pass
