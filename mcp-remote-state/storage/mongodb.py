from storage.storage_base import StorageBase
from config.mongdb_config import settings
import pymongo
import logging


logging.basicConfig(format="%(levelname)s:     %(message)s", level=logging.INFO)

connection_url = f"mongodb://{settings.MONGODB_USER}:{settings.MONGODB_PASSWD}@{settings.MONGODB_URL}"


class Storage(StorageBase):
    def __init__(self, path):
        self.path = path

    def _db(self, connection_url=connection_url):
        try:
            client = pymongo.MongoClient(connection_url)
            db = client[settings.MONGODB_DB_NAME]
            collection = db["tf"]
            return collection
        except Exception as err:
            raise err

    def get(self, id):
        try:
            logging.info(f"Get query id {id}")
            collection = self._db()
            # Query state by index
            query = {"_id": id}
            current_state = collection.find_one(query)
            # 존재하는지 확인
            if (current_state):
                current_state.pop("_id")
                return current_state
            return None
        except Exception as err:
            logging.error(err)
            raise err

    def put(self, id, info):
        try:
            logging.info(f"Put state id {id}")
            collection = self._db()
            # Query last state
            query = {"_id": id}
            current_state = collection.find_one(query)
            if (current_state):
                # terraform state 업데이트
                new_state = {"$set": info}
                collection.update_one(current_state, new_state)
                return True
            # 새 terraform state 추가
            info["_id"] = id
            collection.insert_one(info)
            return True
        except Exception as err:
            logging.error(err)
            raise err

    def lock(self, id, info):
        try:
            logging.info(f"Lock state id {id}")
            collection = self._db()
            # Query last state
            query = {"_id": id + ".lock"}
            current_state = collection.find_one(query)
            if (current_state):
                current_state.pop("_id")
                return False, current_state
            # 새 terraform state 추가
            info["_id"] = id + ".lock"
            collection.insert_one(info)
            return True, id
        except Exception as err:
            logging.error(err)
            raise err

    def unlock(self, id, info):
        try:
            logging.info(f"Unlock state id {id}")
            collection = self._db()
            # Query last state
            query = {"_id": id + ".lock"}
            if collection.find_one(query):
                collection.delete_one(query)
                return True
            return False
        except Exception as err:
            logging.error(err)
            raise err
