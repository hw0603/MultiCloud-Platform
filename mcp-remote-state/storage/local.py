from storage.storage_base import StorageBase
import logging
import json
import os

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


class Storage(StorageBase):
    def __init__(self, path):
        self.path = path
        os.makedirs(self.path, exist_ok=True)

    def get(self, id):
        ...

    def put(self, id, info):
        ...

    def lock(self, id, info):
        ...

    def unlock(self, id, info):
        ...
