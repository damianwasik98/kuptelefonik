from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any


class ResponseStatus(Enum):
    SUCCESS = 200
    SERVER_ERROR = 500
    TOO_MANY_REQUESTS = 429


@dataclass
class Response:
    text: str
    status_code: int #later think abount changing to ResponseStatus

    def __str__(self):
        return f"<{self.__class__.__name__} {self.status_code}>"


class HttpClient(ABC):
    
    @abstractmethod
    def get(self, url: str, *args, **kwargs) -> Any:
        ...


