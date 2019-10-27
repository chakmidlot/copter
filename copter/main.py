import logging
import sys

from copter.app import App
from copter.storage.filesystem import FilesystemStorage
from copter.syphering.syphering_client import SypheringClient
from copter.ui.cli_ui import CliUi
from copter.utils import configure_logging


log = logging.getLogger(__name__)


def main():
    configure_logging()

    log.debug('start')

    try:
        ui = CliUi()
        storage = FilesystemStorage()
        syphering = SypheringClient()

        with ui.init():
            app = App(ui, storage, syphering)

            if len(sys.argv) > 1:
                if sys.argv[1] == 'create':
                    app.create()
                elif sys.argv[1] == 'get':
                    app.read()
            else:
                app.start()
    except Exception:
        log.exception('')

if __name__ == '__main__':
    main()
