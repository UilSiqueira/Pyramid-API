
from abc import ABC, abstractmethod
from core.db.connection import Session

NOT_ALLOWED = 'Operation Not Allowed'


class BaseModel(ABC):
    def __init__(self, db_session = Session):
        self.db_session = db_session
    
    @abstractmethod
    def add(self) -> str: pass

    @abstractmethod
    def list(self) -> str: pass

    def delete(self) -> str:
        raise NotImplementedError(NOT_ALLOWED)

    def update(self) -> str:
        raise NotImplementedError(NOT_ALLOWED)
    
    def _to_dict(self) -> str:
        raise NotImplementedError(NOT_ALLOWED)



