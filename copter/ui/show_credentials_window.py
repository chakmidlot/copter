import curses
import curses.ascii
import curses.panel
import logging

import pyperclip

from copter.commands import CredentialsView


log = logging.getLogger(__name__)


class ShowCredentialsWindow:
    
    def __init__(self, window, creds: CredentialsView):
        self._creds = creds
        self._window = window

        self._current = 0
    
    def draw(self):
        cred_items = [
            self._creds.title, self._creds.service, self._creds.username,
            self._creds.password, ' '.join(self._creds.tags)
        ]
        rows = [
            f'title: {self._creds.title}',
            f'service: {self._creds.service}',
            f'username: {self._creds.username}',
            'password: ******',
            f'tags: {" ".join(self._creds.tags)}',
        ]
        while True:
            self._window.clear()

            self._window.addstr(0, 0, "e: Edit | backspace: Back")
            for i, row in enumerate(rows):
                if i == self._current:
                    pyperclip.copy(cred_items[i])
                    font = curses.A_REVERSE
                else:
                    font = curses.A_NORMAL

                self._window.addstr(i + 2, 0, row, font)

            self._window.refresh()

            result = self.control()
            if result == 'exit':
                return 'exit'
            if result == 'back':
                return 'back'

    def control(self):
        key = self._window.getkey()

        if key == 'KEY_UP' and self._current > 0:
            self._current -= 1
        elif key == 'KEY_DOWN' and self._current < 4:
            self._current += 1
        elif key in ['KEY_BACKSPACE', 'q']:
            return 'back'
        elif key == curses.ascii.ctrl('R'):
            self._current += 1
            if self._current == 5:
                return 'exit'


if __name__ == '__main__':
    from copter.ui.cli_ui import CliUi

    creds = CredentialsView('Google mail', 'google.com', 'chakmidlot', 'password123', ('home', 'test'))
    ui = CliUi()
    with ui.init():
        ShowCredentialsWindow(ui.stdscr, creds).draw()
