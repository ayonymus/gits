
import jsonpickle

from features.storage.models import StorageModel, Tags

PATH_STORAGE2 = "/.git/gits2"


class Storage2:

    __storage_file__ = None

    def __init__(self, path):
        self.__storage_file__ = path + PATH_STORAGE2

    def load_model(self):
        try:
            with open(self.__storage_file__, 'r') as json_file:
                data: StorageModel = jsonpickle.decode(json_file.read())
                return data
        except Exception:
            return StorageModel(Tags(None, None, None))

    def store_model(self, storage_model):
        with open(self.__storage_file__, 'w') as json_file:
            encoded = jsonpickle.encode(storage_model)
            json_file.write(encoded)
