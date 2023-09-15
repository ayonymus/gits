
class Tags(object):
    def __init__(self, main: str = None, work: [] = None, important: {} = None):
        self.main = main
        self.work = work
        self.important = important

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.main == other.main \
               and self.work == other.work \
               and self.important == other.important


class Checkout(object):
    def __init__(self, checkouts=None):
        self.checkouts = checkouts

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and self.checkouts == other.checkouts


class Note(object):
    def __init__(self, text: str, branch: str, created_at, archived_at=None):
        self.text = text
        self.branch = branch
        self.created_at = created_at
        self.archived_at = archived_at

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and self.text == other.text \
            and self.branch == other.branch \
            and self.created_at == other.created_at \
            and self.archived_at == other.archived_at

    def __hash__(self):
        return hash((self.text, self.branch, self.created_at, self.archived_at))

    def __str__(self):
        return f'{self.text}, {self.branch}, {self.created_at}, {self.archived_at}'

    def short_str(self):
        return f'{self.created_at} [{self.branch}] {self.text}'


class Notes(object):
    def __init__(self, notes: [] = None):
        self.notes = notes

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and self.notes == other.notes


class Devops(object):
    def __init__(self, provider=None, config=None):
        self.provider = provider
        self.config = config

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and self.provider == other.provider \
            and self.config == other.config


class StorageModel:
    def __init__(self, tags: Tags = None, checkouts: Checkout = None, notes: Notes = None, devops: Devops = None):
        self.tags = tags
        self.checkouts = checkouts
        self.notes = notes
        self.devops = devops

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and self.tags == other.tags \
            and self.checkouts == other.checkouts \
            and self.devops == other.devops
