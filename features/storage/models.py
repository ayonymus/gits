
class Tags(object):
    def __init__(self, main=None, work=None, important=None):
        self.main = main
        self.work = work
        self.important = important

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.main == other.main \
               and self.work == other.work \
               and self.important == other.important \


class Checkout(object):
    def __init__(self, checkouts=None):
        self.checkouts = checkouts

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and self.checkouts == other.checkouts


class StorageModel:
    def __init__(self, tags: Tags = None, checkouts: Checkout = None):
        self.tags = tags
        self.checkouts = checkouts

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.tags == other.tags \
               and self.checkouts == other.checkouts
