
class CheckoutHistory:

    def __init__(self, git, storage):
        self.git = git
        self.storage = storage

    def checkout(self, branch, new_branch=False):
        if self.git.checkout(branch, new_branch):
            history = self.storage.load_checkout_history()
            if history is None or len(history) == 0:
                self.storage.store_checkout_history([branch])
            elif history[-1] != branch:
                history.append(branch)
                self.storage.store_checkout_history(history)
            return True
        else:
            return False

    def get_checkout_history(self):
        return self.storage.load_checkout_history()
