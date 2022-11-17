
from enum import Enum

from features.storage.store import Storage2
from tools.githelper import GitHelper


class SpecialTags(Enum):
    MAIN = "main"
    WORK = "work"
    IMPORTANT = "important"


class TagsStorage:

    def __init__(self, storage: Storage2):
        self.storage = storage

    def load_tags(self):
        return self.storage.load_model().tags

    def store_tags(self, tags):
        data = self.storage.load_model()
        data.tags = tags
        self.storage.store_model(data)


class TagsHandler:

    def __init__(self, store: TagsStorage, git: GitHelper):
        self.store = store
        self.git = git

    def is_main_set(self):
        return self.store.load_tags().main is not None

    def set_main(self):
        current = self.git.current_branch()
        tags = self.store.load_tags()
        tags.main = current
        self.store.store_tags(tags)

    def set_work(self):
        current = self.git.current_branch()
        tags = self.store.load_tags()
        if tags.work is None:
            tags.work = [current]
        elif tags.work[0] != current:
            tags.work.insert(0, current)
        self.store.store_tags(tags)
        return current

    def add_important(self):
        current = self.git.current_branch()
        tags = self.store.load_tags()
        imp = tags.important
        if imp is None:
            tags.important = {current}
        else:
            tags.important.add(current)
        self.store.store_tags(tags)

    def get_tags(self):
        return self.store.load_tags()
