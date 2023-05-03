from dataclasses import dataclass
import json


@dataclass
class ApiStatus:
    SUCCESS: int = 200
    BAD_REQUEST: int = 400
    UNAUTHORIZED: int = 401
    NOT_FOUND: int = 404
    ERROR: int = 500

class ApiResponse:
    def __init__(self, status: ApiStatus, message: str):
        self.status = status
        self.message = message

    @classmethod
    def with_data(cls, status: ApiStatus, message: str, data: object):
        response = cls(status, message)
        response.data = data
        return response
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
