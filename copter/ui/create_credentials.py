import curses
import logging

import pyperclip

from copter.commands import CredentialsView
from copter.utils import password_generator

log = logging.getLogger(__name__)


class CreateCredentialsWindow:

    def __init__(self, window):
        self._window = window

        self._fields = [
            ('title', 'text', curses.newwin(1, 180, 3, 7), lambda x: x),
            ('service', 'text', curses.newwin(1, 180, 4, 9), lambda x: x),
            ('username', 'text', curses.newwin(1, 180, 5, 10), lambda x: x),
            ('password', 'password', curses.newwin(1, 180, 6, 10), lambda x: x),
            ('tags', 'text', curses.newwin(1, 180, 7, 6), lambda x: x.split(' ')),
        ]

    def draw(self):
        self._window.addstr(0, 0, """Copter password manager

Enter new credentials:""")
        for i, (field, *_) in enumerate(self._fields):
            self._window.addstr(i + 3, 0, f'{field}: ')

        self._window.addstr(len(self._fields) + 4, 0, 'ctrl-R generate password')
        self._window.refresh()
        creds = CredentialsView()
        curses.curs_set(1)

        i = 0
        while True:
            value, action = self.get_value(self._fields[i][2], self._fields[i][1] == 'password')
            creds.__setattr__(self._fields[i][0], self._fields[i][3](value))
            if action == 'DOWN':
                if i == len(self._fields) - 1:
                    break
                else:
                    i += 1
            elif action == 'UP' and i > 0:
                i -= 1

        curses.curs_set(0)
        return creds

    def get_value(self, window, password=False):
        data = ''
        while True:
            key = window.getkey()
            log.info(key)
            if key == '\n':
                return data, 'DOWN'
            elif key == '\x7f':
                data = data[:-1]
                window.clear()
            elif key == '\x12':
                password = password_generator(20)
                pyperclip.copy(password)
                data = password
                log.info(data)
                window.addstr(0, 0, '*' * len(data))
                return data, 'DOWN'
            elif len(key) == 1:
                data += key

            if password:
                window.addstr(0, 0, '*' * len(data))
            else:
                window.addstr(0, 0, data)

            window.refresh()


if __name__ == '__main__':
    import curses.ascii
    print(curses.KEY_BACKSPACE)
    print(chr(curses.KEY_BACKSPACE))
    print('\x7f')
    print('\xc2\x86')
    print(ord('й'))
