import json

from features.tags.tags_handler import Tags

PATH_STORAGE2 = "/.git/gits2"


class StorageModel:
    def __init__(self, tags):
        self.tags = tags

    def __eq__(self, other):
        return self.tags == other.tags


class Storage2:

    __storage_file__ = None

    def __init__(self, path):
        self.__storage_file__ = path + PATH_STORAGE2

    def load_model(self):
        try:
            with open(self.__storage_file__, 'r') as json_file:
                return StorageModel(**json.loads(json_file.read()))
        except FileNotFoundError:
            return StorageModel(Tags(None, None, None))

    def store_model(self, storage_model):
        with open(self.__storage_file__, 'w') as json_file:
            return json.dump(storage_model, json_file)
