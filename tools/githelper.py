import git
from git import Repo
import os


class GitHelper:
    """
    Wrapper class around git commands for easier usage and unit testing.
    """

    def __init__(self):
        try:
            self.repo = Repo(os.getcwd())
        except git.exc.InvalidGitRepositoryError:
            print('Script should be called from root directory of a git repository. Exit')
            exit(1)

    def is_existing_branch(self, branch):
        try:
            self.repo.git.rev_parse('--verify', branch)
            return True
        except:
            return False

    def branch(self):
        return self.repo.active_branch.name

    def checkout(self, branch):
        try:
            self.repo.git.checkout(branch)
            return True
        except git.exc.GitCommandError:
            return False

    def work_dir(self):
        return self.repo.working_dir
