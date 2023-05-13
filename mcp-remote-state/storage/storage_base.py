from abc import *

# 다양한 Storage를 지원하기 위한 추상화 클래스
class StorageBase(metaclass=ABCMeta):

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def put(self, id, info):
        pass

    @abstractmethod
    def lock(self, id, info):
        pass

    @abstractmethod
    def unlock(self, id, info):
        pass
