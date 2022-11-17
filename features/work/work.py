from features.checkout2.checkout import CheckoutHandler
from features.tags.tags import TagsHandler
from tools.githelper import GitHelper


class WorkHandler:

    def __init__(self, tags: TagsHandler, checkout: CheckoutHandler, git: GitHelper):
        self.tags = tags
        self.checkout = checkout
        self.git = git

    def set_work(self):
        return self.tags.set_work()

    def checkout_work_branch(self):
        self.checkout.checkout_work()
        return self.tags.get_tags().work[0]

    def get_logs(self, length, full):
        branches = set(self.git.branches_str())
        logs = self.tags.get_tags().work
        if logs is None:
            return []
        if not full:
            logs = logs[:length]

        is_removed = []
        for log in logs:
            removed = log not in branches
            is_removed.append((log, removed))
        return is_removed
