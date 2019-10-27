import logging
import pickle
from pathlib import Path

from copter import settings
from copter.commands import CredentialsStorage


log = logging.getLogger(__name__)


class FilesystemStorage:

    def __init__(self):
        self.data_path = Path(settings.DB_PATH).expanduser() / 'secrets'
        self.data_path.mkdir(parents=True, exist_ok=True)

    def save(self, creds: CredentialsStorage):
        service_file = self.data_path / creds.service
        with service_file.open('wb') as f:
            pickle.dump(creds, f)

    def get(self, service) -> CredentialsStorage:
        log.info(f'{service=}')
        service_file = self.data_path / service
        with service_file.open('rb') as f:
            return pickle.loads(f.read())

    def get_all_secrets(self):
        keys = []
        for keyfile in self.data_path.iterdir():
            if not keyfile.name.startswith('.'):
                with (self.data_path / keyfile.name).open('rb') as fp:
                    keys.append(pickle.loads(fp.read()))
        return keys


if __name__ == '__main__':
    c = CredentialsStorage('title', 'a', 'b', b'abcd', ('abcd', ))
    print(c)
