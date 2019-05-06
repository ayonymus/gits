from tools.githelper import GitHelper


class Cleanup:
    """
    This should clean up a branch when done working.

    do on a work branch - not master or development
    should be on master or development when running

    check branch if fully merged
    check if branch has tasks not done

    delete branch
    delete done tasks and branch

    """

    BRANCH_MASTER = "master"
    BRANCH_DEV = "dev"
    BRANCH_DEVELOPMENT = "development"

    SUCCESS = 0
    ERROR = 1
    NOT_MASTER_OR_DEV = 2
    HAS_OPEN_TASKS = 3
    NOT_EXIST = 4
    NOT_MERGED = 5

    def __init__(self, git, storage, workbranch, tasks):
        self.git = git
        self.storage = storage
        self.workbranch = workbranch
        self.tasks = tasks

    def cleanup(self, branch):
        current = self.git.branch()
        if current != self.BRANCH_MASTER and current != self.BRANCH_DEV and current != self.BRANCH_DEVELOPMENT:
            return self.NOT_MASTER_OR_DEV
        if self.tasks.get_tasks(branch):
            return self.HAS_OPEN_TASKS
        result = self.git.delete_branch(branch)

        if result == GitHelper.NOT_MERGED:
            return self.NOT_MERGED
        if result == GitHelper.NOT_FOUND:
            return self.NOT_EXIST
        if result == GitHelper.ERROR:
            return self.ERROR
        self.tasks.remove_done_tasks(branch)
        return self.SUCCESS
