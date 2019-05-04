
class CheckoutHistory:

    def __init__(self, git, storage):
        self.git = git
        self.storage = storage

    def checkout(self, branch):
        if self.git.checkout(branch):
            history = self.storage.load_checkout_history()
            if not history:
                self.storage.store_checkout_history([branch])
            if history and history[-1] is not branch:
                history.append(branch)
                self.storage.store_checkout_history(history)
        else:
            print("Select another branch")