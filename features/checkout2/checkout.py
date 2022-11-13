from datetime import datetime

from features.storage.models import Checkout
from features.storage.store import Storage2
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
        data = self.store.load_model().checkouts
        data.tags = checkouts
        self.store.store_model(data)


class CheckoutHandler:

    def __init__(self, store: CheckoutStore, git: GitHelper, time=datetime):
        self.store = store
        self.git = git
        self.time = time

    def checkout(self, branch, new_branch=False):
        if self.git.checkout(branch, new_branch):
            check = self.store.load_checkouts()
            checkouts = check.checkouts
            if checkouts is None or len(checkouts) == 0:
                check.checkouts = [(branch, self.time.now())]
            elif checkouts[-1][0] != branch:
                check.checkouts.append((branch, self.time.now()))

            self.store.store_checkouts(check)
            return True
        else:
            return False


