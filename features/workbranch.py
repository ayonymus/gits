
class WorkBranch:
    """
        Handle work branches with git and local storage
    """
    def __init__(self, git, storage, checkout):
        self.git = git
        self.storage = storage
        self.checkout = checkout

    def get_work_branch(self):
        return self.storage.get_work_branch()

    def get_work_branch_history(self):
        branches = self.storage.load_work_branches()
        branches.reverse()
        return branches

    def set_work_branch(self):
        branch = self.git.branch()
        branches = self.storage.load_work_branches()
        if len(branches) == 0:
            self.storage.set_work_branch(branch)
        elif branches[-1] != branch:
            branches.append(branch)
            self.storage.set_work_branch(branch)
        return branch

    def checkout_work_branch(self, branch=None):
        if branch is None:
            branch = self.get_work_branch()
        if branch is not None:
            result = self.checkout.checkout(branch)
            return branch, result
        return branch, False

    def checkout_work_branch_from_history(self, index):
        branches = self.get_work_branch_history()
        branch = None
        if len(branches) > 0 and len(branches) > index:
            branch = branches[index]
            return self.checkout_work_branch(branch)
        return branch, False

    def unset_work_branch(self):
        self.storage.set_work_branch(None)
