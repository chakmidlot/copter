from pathlib import Path

from copter import settings
from copter.daemon import Login, Status, Encode, Result, GetStatus, Decode
from copter.syphering.aes_syphering import encode, decode

_key = None


def do(command_message):
    command = command_message
    if isinstance(command, Login):
        return Commands.login(command.password)
    elif isinstance(command, Encode):
        return Commands.encode(command.message)
    elif isinstance(command, GetStatus):
        return Commands.status()
    elif isinstance(command, Decode):
        return Commands.decode(command.message)


class Commands:

    @staticmethod
    def login(password):
        global _key

        key_path = Path(settings.DB_PATH).expanduser() / '.password'
        if not key_path.exists():
            with key_path.open('wb') as f:
                f.write(encode(password, settings.AES_CBC, password))
        else:
            with key_path.open('rb') as f:
                if f.read() == encode(password, settings.AES_CBC, password):
                    _key = password
                    return Status.LOGGED_IN
                else:
                    return Status.LOGGED_OUT

    @staticmethod
    def logout():
        global _key
        _key = None
        return Status.LOGGED_OUT

    @staticmethod
    def status():
        if _key:
            return Status.LOGGED_IN
        else:
            return Status.LOGGED_OUT

    @staticmethod
    def encode(message):
        if _key:
            return Result(encode(_key, settings.AES_CBC, message))
        else:
            return Status.LOGGED_OUT

    @staticmethod
    def decode(message):
        if _key:
            return Result(decode(_key, settings.AES_CBC, message))
        else:
            return Status.LOGGED_OUT


if __name__ == '__main__':
    print(Commands.login(input().encode()))