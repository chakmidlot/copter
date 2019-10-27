from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class Command(Enum):
    READ = 1
    CREATE = 2


@dataclass
class CredentialsStorage:
    title: str = ''
    service: str = ''
    username: str = ''
    password: bytes = b''
    tags: Tuple[str] = ()


@dataclass
class CredentialsView:
    title: str = ''
    service: str = ''
    username: str = ''
    password: str = ''
    tags: Tuple[str] = ()
