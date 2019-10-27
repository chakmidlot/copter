import pickle
import socket

from copter import settings
from copter.daemon import Encode, Decode, Status, GetStatus, Login
from copter.syphering import Unauthorized


class SypheringClient:

    server = (settings.DAEMON.HOST, settings.DAEMON.PORT)

    def status(self):
        return self._send(GetStatus())

    def login(self, password):
        return self._send(Login(password.encode()))

    def encode(self, message):
        resp = self._send(Encode(message.encode()))

        if resp == Status.LOGGED_OUT:
            raise Unauthorized()
        return resp

    def decode(self, message):
        resp = self._send(Decode(message))

        if resp == Status.LOGGED_OUT:
            raise Unauthorized()
        return resp

    def _send(self, message):
        response = b''

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.server)
            s.sendall(pickle.dumps(message))
            while True:
                data = s.recv(1024)
                if not data:
                    break
                response += data

        response = pickle.loads(response)

        return response


if __name__ == '__main__':
    s = SypheringClient().decode(b'\xca\x8e^$\xd4y5\n\x04\xac\x08,\x97\xdd\x88c\r\x98O\x83\x95\xac\xfa\xcah\xcfL\xa9\xfa\x0bO\xfc')

    print(s)
