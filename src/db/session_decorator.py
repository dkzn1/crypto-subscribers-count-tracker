from typing import Optional, Callable
from functools import wraps
from sqlalchemy.orm import Session
from lib.logger import Logger


def session_decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result: Optional[list]

        with Session(self.engine) as session:
            try:
                result = func(self, *args, **kwargs, session=session)
                session.expire_on_commit = False
                session.commit()

            except Exception as e:
                log = Logger(name=func.__name__)

                log.error(e)
                session.rollback()
                return

        return result

    return wrapper
