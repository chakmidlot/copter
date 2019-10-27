import curses


class LoginWindow:
    
    def __init__(self, window):
        self._window = window
    
    def draw(self):
        self._window.clear()

        self._window.addstr(0, 0, """Copter password manager

Sign in
password:""")
        self._window.refresh()
        curses.curs_set(1)

        curses.noecho()
        self._window.move(3, 10)
        password = self._window.getstr().decode()

        curses.curs_set(0)
        return password
