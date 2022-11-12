
from enum import Enum


class SpecialTags(Enum):
    MAIN = "main"
    WORK = "work"
    IMPORTANT = "important"


class Tags(object):
    def __init__(self, main, work, important):
        self.main = main
        self.work = work
        self.important = important

    def __eq__(self, other):
        return self.main == other.main \
               and self.work == other.work \
               and self.important == other.important \
               and isinstance(other, self.__class__)


class TagsHandler:

    def __init__(self, storage):
        self.storage = storage

    def load_tags(self):
        return self.storage.load_model().tags

    def store_tags(self, tags):
        data = self.storage.load_model()
        data.tags = tags
        self.storage.store_model(data)
