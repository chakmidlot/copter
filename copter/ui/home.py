import curses


class HomeWindow:

    def __init__(self, window):
        self._window = window

    def draw(self):
        self._window.clear()
        self._window.addstr(0, 0, """Copter password manager

Choose command:
1. Read
2. Create""")
        self._window.refresh()
