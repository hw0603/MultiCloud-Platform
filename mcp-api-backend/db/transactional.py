from functools import wraps
from . import session

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
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e

            return result

        return _transactional
