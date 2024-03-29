from datetime import datetime

from data.models import Checkout
from data.store import Storage2
from features.tags.tags import TagsHandler
from tools.githelper import GitHelper


class CheckoutStore:
    def __init__(self, store: Storage2):
        self.store = store

    def load_checkouts(self):
        checkouts = self.store.load_model().checkouts
        if checkouts is None:
            return Checkout()
        else:
            return checkouts

    def store_checkouts(self, checkouts):
        data = self.store.load_model()
        data.checkouts = checkouts
        self.store.store_model(data)


class CheckoutHandler:

    def __init__(self, store: CheckoutStore, git: GitHelper, tags: TagsHandler, time=datetime):
        self.store = store
        self.git = git
        self.time = time
        self.tags = tags

    def checkout(self, branch, new_branch=False):
        if branch == '.':
            self.git.checkout(branch, False)
        elif self.git.checkout(branch, new_branch):
            check_model: Checkout = self.store.load_checkouts()
            checkouts = check_model.checkouts
            if checkouts is None or len(checkouts) == 0:
                check_model.checkouts = [(branch, str(self.time.now()))]
            elif checkouts[0] != branch:
                check_model.checkouts.insert(0, (branch, str(self.time.now())))
            self.store.store_checkouts(check_model)
            return branch
        else:
            return None

    def checkout_suffix(self, suffix):
        current = self.git.current_branch()
        return self.checkout(f'{current}_{suffix}', True)

    def get_logs(self, length, full):
        branches = set(self.git.branches_str())
        logs = self.store.load_checkouts().checkouts
        if logs is None:
            return []
        if not full:
            logs = logs[:length]

        is_removed = []
        for log in logs:
            removed = log[0] not in branches
            is_removed.append((log[0], log[1], removed))
        return is_removed

    def checkout_main(self):
        main = self.tags.get_tags().main
        return self.checkout(main) if main else None

    def checkout_work(self):
        work = self.tags.get_tags().work
        return self.checkout(work[0]) if work else None

    def checkout_prev(self):
        logs = self.store.load_checkouts().checkouts
        return self.checkout(logs[1][0]) if len(logs) > 1 else None



