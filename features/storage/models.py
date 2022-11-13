

class Tags(object):
    def __init__(self, main=None, work=None, important=None):
        self.main = main
        self.work = work
        self.important = important

    def __eq__(self, other):
        return self.main == other.main \
               and self.work == other.work \
               and self.important == other.important \
               and isinstance(other, self.__class__)


class StorageModel:
    def __init__(self, tags):
        self.tags = tags

    def __eq__(self, other):
        return self.tags == other.tags


