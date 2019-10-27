from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def encode(password, cbc, message):
    message += b'\0' * (32 - len(message) % 32)
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password)
    key = digest.finalize()[:32]

    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(cbc), backend=backend)
    encryptor = cipher.encryptor()
    return encryptor.update(message) + encryptor.finalize()


def decode(password, cbc, message):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password)
    key = digest.finalize()[:32]

    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(cbc), backend=backend)
    decryptor = cipher.decryptor()
    decripted = decryptor.update(message) + decryptor.finalize()
    return decripted.strip(b'\0')
