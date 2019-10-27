import curses
import logging
from typing import Iterable

from copter.commands import CredentialsView
from copter.utils import configure_logging

log = logging.getLogger(__name__)
configure_logging()


class KeyChooseWindow:

    def __init__(self, window: curses.window, all_keys: Iterable[CredentialsView]):
        self._window = window
        x, y = self._window.getmaxyx()
        self._page_size = x - 5
        self._key_window: curses.window = curses.newwin(x - 5, y, 5, 0)
        self._all_keys = all_keys

        self._current = 0
        self._filter = ''
        self._prev_current = None

    def choose_key(self):
        log.info(self._all_keys)
        curses.curs_set(1)

        while True:
            self._window.clear()
            self.draw_info()

            self.draw_keys()

            self._window.refresh()
            self._key_window.refresh()

            self._window.addstr(3, 0, self._filter)
            if action := self.handle_controls():
                return action, self.filtered_keys[self._current]

    def draw_info(self):
        self._window.addstr(0, 0, """Del: remove | Enter: open

select""")

    def draw_keys(self):
        log.info(self._key_window.getmaxyx())
        page_start = self._current // self._page_size * self._page_size
        page_stop = page_start + self._page_size
        log.info(f'{page_start} {page_stop}')
        for i, key in enumerate(self.filtered_keys[page_start:page_stop]):
            if i == self._current % self._page_size:
                font = curses.A_REVERSE
            else:
                font = curses.A_NORMAL
            text = f'{key.title} | {key.service} | {key.username} | ({" ".join(key.tags)})'
            try:
                self._key_window.addstr(i, 0, text, font)
            except Exception:
                log.error(f'{i} {text}')
                raise

    def handle_controls(self):
        key = self._window.getkey()
        if key == 'KEY_UP' and self._current > 0:
            self._current -= 1
        elif key == 'KEY_DOWN' and self._current < len(self.filtered_keys) - 1:
            self._current += 1
        elif key == '\n':
            return 'open'
        elif key == 'KEY_DC':
            creds = self.filtered_keys[self._current]
            if self.confirm_remove(f'{creds.title or creds.service} | {creds.username}'):
                return 'remove'
        elif key == 'KEY_BACKSPACE':
            self._current = 0
            self._filter = self._filter[:-1]
        elif key == 'KEY_RESIZE':
            x, y = self._window.getmaxyx()
            self._page_size = x - 5
            self._key_window.resize(x - 5, y)
        elif len(key) == 1:
            self._current = 0
            self._filter += key

    def confirm_remove(self, key_name):
        x, y = self._window.getmaxyx()
        w = curses.newwin(6, len(key_name) + 4, x // 2 - 3, len(key_name) // 2)
        w.addstr(1, x // 2 - 10, "Remove secret?")
        w.addstr(2, 1, key_name)
        w.addstr(4, x // 2 - 3, 'y/n')
        w.border()
        w.refresh()

        return w.getkey().lower() == 'y'

    @property
    def filtered_keys(self):
        keys = []
        for key in self._all_keys:
            if (key.title or '').lower().startswith(self._filter) \
                    or key.service.lower().startswith(self._filter) \
                    or key.username.lower().startswith(self._filter) \
                    or any([tag.lower().startswith(self._filter) for tag in key.tags]):
                keys.append(key)

        return keys


if __name__ == '__main__':
    from copter.ui.cli_ui import CliUi

    data = [
        CredentialsView("Google mail", "http://gmail.com", "chakmidlot", '', ("home", "mail", "service")),
        CredentialsView('', "http://gmail.com", "d.tolkach", '', ("work", "mail")),
        CredentialsView("twitter", "twitter.com", "chakmidlot", '', ("home",)),
        *[CredentialsView(f"service{i}", "test service", f"chakmidlot_{i}", '', ("home",)) for i in range(40)]
    ]

    ui = CliUi()
    with ui.init():
        KeyChooseWindow(ui.stdscr, data).choose_key()
