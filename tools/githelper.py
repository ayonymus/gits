import git
from git import Repo
import os


class GitHelper:
    """
    Wrapper class around git commands for easier usage and unit testing.
    """

    SUCCESS = 0
    ERROR = 1
    NOT_FOUND = 2
    NOT_MERGED = 3

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
        except git.exc.GitCommandError:
            return False

    def branch(self):
        return self.repo.active_branch.name

    def branches(self):
        return self.repo.branches

    def checkout(self, branch, new_branch=False):
        try:
            if new_branch:
                self.repo.git.checkout('-b', branch)
            else:
                self.repo.git.checkout(branch)
            return True
        except git.exc.GitCommandError as e:
            print(e)
            return False

    def work_dir(self):
        return self.repo.working_dir

    def delete_branch(self, branch):
        try:
            self.repo.git.branch('-d', branch)
            return self.SUCCESS
        except git.exc.GitCommandError as e:
            if 'not found.' in e.stderr:
                return self.NOT_FOUND
            elif 'not fully merged' in e.stderr:
                return self.NOT_MERGED
            else:
                print(e.stderr)
            return self.ERROR

