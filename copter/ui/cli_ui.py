import os
from contextlib import contextmanager
import curses
import curses.textpad

from copter.commands import Command, CredentialsView
from copter.ui.choose_key import KeyChooseWindow
from copter.ui.create_credentials import CreateCredentialsWindow
from copter.ui.home import HomeWindow
from copter.ui.login_window import LoginWindow
from copter.ui.show_credentials_window import ShowCredentialsWindow


class CliUi:

    def __init__(self):
        self.stdscr = None
        os.environ.setdefault('ESCDELAY', '0')

    @contextmanager
    def init(self):
        try:
            self.stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()
            self.stdscr.keypad(1)
            curses.curs_set(0)

            yield

        finally:
            self.stdscr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()

    def home(self):
        HomeWindow(self.stdscr).draw()

    def get_command(self):
        while True:
            key = self.stdscr.getkey()
            if key.isdigit() and 1 <= int(key) <=len(Command):
                return Command(int(key))

    def get_credentials(self) -> CredentialsView:
        return CreateCredentialsWindow(self.stdscr).draw()

    def choose_key(self, all_keys):
        return KeyChooseWindow(self.stdscr, all_keys).choose_key()

    def show_creds(self, creds: CredentialsView):
        return ShowCredentialsWindow(self.stdscr, creds).draw()

    def login(self):
        return LoginWindow(self.stdscr).draw()
