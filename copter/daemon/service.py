import pickle
import socket
import traceback

from copter import settings
from copter.daemon.commands import do


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((settings.DAEMON.HOST, settings.DAEMON.PORT))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            command = read_command(conn)
            response = do(command)
            conn.sendall(pickle.dumps(response))
            conn.shutdown(1)


def read_command(conn):
    try:
        message = conn.recv(1024)
        command = pickle.loads(message)
        return command
    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    start_server()
