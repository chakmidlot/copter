import pickle
from struct import pack, unpack

from copter.storage import Secret, StorageItem, DataType


class IncrementalFile:

    def __init__(self):
        self.path = '/tmp/secrets'

    def add(self, key):
        with open(self.path, 'ab') as fp:
            data = pickle.dumps(StorageItem(DataType.ADD, key))
            fp.write(pack('<I', len(data)) + data)

    def get(self, name):
        self._get_all().get(name)

    def remove(self, key):
        with open(self.path, 'ab') as fp:
            data = pickle.dumps(StorageItem(DataType.REMOVE, Secret(key)))
            fp.write(pack('<I', len(data)) + data)

    def list(self):
        return self._get_all().keys()

    def _get_all(self):
        secrets = {}
        with open(self.path, 'rb') as fp:
            while True:
                size = fp.read(4)
                if not size:
                    break
                size = unpack('<I', size)
                item = pickle.loads(fp.read(size[0]))
                if item.dataType == DataType.ADD:
                    secrets[item.payload.name] = item.payload
                elif item.dataType == DataType.REMOVE:
                    if item.payload.name in secrets:
                        del secrets[item.payload.name]
        return secrets
