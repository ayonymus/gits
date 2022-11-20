
import jsonpickle

from data.models import StorageModel

PATH_STORAGE2 = "/.git/gits2"

# TODO rename to repository


class Storage2:

    __storage_file__ = None

    __cache__ = None

    def __init__(self, path):
        self.__storage_file__ = path + PATH_STORAGE2

    def load_model(self):
        if self.__cache__ is None:
            try:
                with open(self.__storage_file__, 'r') as json_file:
                    data: StorageModel = jsonpickle.decode(json_file.read())
                    self.__cache__ = data
                    return data
            except Exception:
                return StorageModel()
        else:
            return self.__cache__

    def store_model(self, storage_model):
        self.__cache__ = storage_model
        with open(self.__storage_file__, 'w') as json_file:
            encoded = jsonpickle.encode(storage_model)
            json_file.write(encoded)
