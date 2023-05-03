from functools import wraps
from .session import AsyncSessionLocal

"""
DB 업데이트 시 명시적 commit() 보다는 @Transactional 어노테이션을 지원하기 위한 데코레이터

ex)
from db import Transactional, session
@Transactional()
async def add_user(self):
    session.add(User(name="John Doe"))
"""

class Transactional:
    def __call__(self, func):
        @wraps(func)
        async def _transactional(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                db_session = AsyncSessionLocal
                await db_session.commit()
            except Exception as e:
                await db_session.rollback()
                raise e
            finally:
                await db_session.close()
            return result

        return _transactional
