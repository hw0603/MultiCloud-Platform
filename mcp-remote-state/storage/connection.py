from config.storage_config import settings


# Storage 정책 관리 클래스
class StoragePolicy:
    def __init__(self, mod) -> None:
        self.mod = mod.lower()

    # Storage 정책에 따라 모듈을 동적으로 로드
    def dynamic_load(self):
        return __import__(f"storage.{self.mod}", fromlist=[None])


storage_setting = StoragePolicy(settings.MCP_STORAGE_BACKEND)  # 설정에서 Storage 정책을 가져옴
loaded_module = storage_setting.dynamic_load()  # Storage 정책에 따라 모듈을 동적으로 로드
Storage = loaded_module.Storage  # 로드된 모듈에서 Storage 클래스를 가져옴
remote_state = Storage(path="/tmp/.remote_states")  # Storage 인스턴스 생성

def get_remote_state() -> Storage:
    try:
        yield remote_state
    except Exception as e:
        raise e
