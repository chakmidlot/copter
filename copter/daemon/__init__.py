from dataclasses import dataclass
from enum import Enum


@dataclass
class Login:
    password: bytes

@dataclass
class GetStatus:
    pass

@dataclass
class Logout:
    pass


@dataclass
class Encode:
    message: bytes


@dataclass
class Decode:
    message: bytes


class Status(Enum):
    LOGGED_IN = 1
    LOGGED_OUT = 2


@dataclass
class Result:
    message: bytes
