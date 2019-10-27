import logging

from copter.commands import Command, CredentialsStorage, CredentialsView
from copter.daemon import Status
from copter.storage.filesystem import FilesystemStorage
from copter.syphering import Unauthorized
from copter.syphering.syphering_client import SypheringClient
from copter.ui.cli_ui import CliUi

log = logging.getLogger(__name__)


class App:

    def __init__(self, ui, storage, syphering):
        self._ui: CliUi = ui
        self._storage: FilesystemStorage = storage
        self._syphering = syphering

    def start(self):
        try:
            self._ui.home()
            command = self._ui.get_command()
            self.do(command)
        except KeyboardInterrupt:
            pass

    def do(self, command):
        if command == Command.CREATE:
            self.create()
        elif command == Command.READ:
            self.read()

    def create(self):
        self.login()
        view_creds = self._ui.get_credentials()
        password = self._syphering.encode(view_creds.password).message

        storage_creds = CredentialsStorage(
            view_creds.title, view_creds.service, view_creds.username,
            password, view_creds.tags
        )
        self._storage.save(storage_creds)

    def read(self):
        self.login()
        while True:
            services = self._storage.get_all_secrets()
            action, key = self._ui.choose_key(services)
            if action == 'open':
                creds = self._storage.get(key.service)
                password = self._syphering.decode(creds.password).message.decode()

                creds_view = CredentialsView(
                    creds.title, creds.service, creds.username,
                    password, creds.tags
                )
                ret = self._ui.show_creds(creds_view)
                if ret == 'exit':
                    break

    def login(self):
        for i in range(3):
            status = self._syphering.status()
            if status == Status.LOGGED_OUT:
                password = self._ui.login()
                self._syphering.login(password)
            else:
                break

        if status == Status.LOGGED_OUT:
            raise Unauthorized()


if __name__ == '__main__':
    creds = FilesystemStorage().get('x')
    password = SypheringClient().decode(creds.password)
    print(creds.password)
    print(password)
