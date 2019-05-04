from tools.githelper import GitHelper


class Workbranch:
    """
        Handle work branches with git and local storage
    """
    def __init__(self, storage, checkout, git=None):
        self.storage = storage
        self.checkout = checkout
        self.git = git if not None else GitHelper()

    def get_work_branch(self):
        branches = self.storage.load_work_branches()
        return None if len(branches) == 0 else branches[-1]

    def get_work_branch_history(self):
        return self.storage.load_work_branches()

    def set_work_branch(self):
        branch = self.git.branch()
        branches = self.storage.load_work_branches()
        if len(branches) == 0:
            self.storage.update_branch_history([branch])
        elif branches[-1] != branch:
            branches.append(branch)
            self.storage.update_branch_history(branches)
        return branch

    def checkout_work_branch(self, branch=None):
        if branch is None:
            branch = self.get_work_branch()
        if branch is not None:
            self.checkout.checkout(branch)
        return branch

    def checkout_work_branch_from_history(self, index):
        branches = self.get_work_branch_history()
        branch = None
        if len(branches) > 0 and len(branches) > index:
            branch = branches[index]
            self.checkout_work_branch(branch)
            return branch
        return branch


