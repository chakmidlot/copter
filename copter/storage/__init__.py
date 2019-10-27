from dataclasses import dataclass
from enum import Enum


class DataType(Enum):
    ADD = 1
    EDIT = 2
    REMOVE = 3


@dataclass
class Secret:
    name: str
    username: str = None
    password: bytes = None


@dataclass
class StorageItem:
    dataType: DataType
    payload: Secret = None
