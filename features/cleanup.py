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

    SUCCESS = 0
    ERROR = 1
    NOT_MAIN_BRANCH = 2
    HAS_OPEN_TASKS = 3
    NOT_EXIST = 4
    NOT_MERGED = 5
    BRANCH_IGNORED = 6
    CURRENT_BRANCH = 7
    MAIN_BRANCH_NOT_SET = 8
    OK_TO_DELETE = 9

    def __init__(self, git, storage, workbranch, tasks):
        self.git = git
        self.storage = storage
        self.workbranch = workbranch
        self.tasks = tasks

    def has_main_branch(self): return len(self.storage.load_main_branches()) > 0
    
    def add_main_branch(self, branch):
        if self.git.is_existing_branch(branch): 
            self.storage.store_main_branch([branch])
            return True
        else:
            return False
    
    def get_main_branch(self): return self.storage.load_main_branches()[0]

    def add_to_ignorelist(self, branch):
        ignore_list = self.storage.load_cleanup_ignorelist()
        if branch not in ignore_list:
            ignore_list.append(branch)
            self.storage.store_cleanup_ignorelist(ignore_list)

    def remove_from_ignorelist(self, branch):
        ignore_list = self.storage.load_cleanup_ignorelist()
        if branch in ignore_list:
            ignore_list.remove(branch)
            self.storage.store_cleanup_ignorelist(ignore_list)
            return True
        else:
            return False

    def get_ignorelist(self):
        return self.storage.load_cleanup_ignorelist()

    def validate_branch(self, branch):
        current = self.git.branch().strip()
        if current not in self.storage.load_main_branches():
            return self.NOT_MAIN_BRANCH
        if current == branch:
            return self.CURRENT_BRANCH
        if branch in self.storage.load_cleanup_ignorelist():
            return self.BRANCH_IGNORED
        if self.tasks.get_tasks(branch):
            return self.HAS_OPEN_TASKS
        if not self.git.is_merged(branch, current):
            return self.NOT_MERGED
        return self.OK_TO_DELETE

    def cleanup(self, branch, hard=False):
        result = self.git.delete_branch(branch, hard)
        if result == GitHelper.NOT_MERGED:
            return self.NOT_MERGED
        if result == GitHelper.NOT_FOUND:
            return self.NOT_EXIST
        if result == GitHelper.ERROR:
            return self.ERROR
        self.tasks.remove_done_tasks(branch)
        return self.SUCCESS