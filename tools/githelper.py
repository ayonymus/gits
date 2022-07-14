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
            self.repo = Repo(os.getcwd(), search_parent_directories=True)
        except git.exc.InvalidGitRepositoryError:
            print('Script should be called from root directory of a git repository. Exit')
            exit(1)

    def is_existing_branch(self, branch):
        try:
            self.repo.git.rev_parse('--verify', branch)
            return True
        except git.exc.GitCommandError:
            return False

    def has_remote(self, branch):
        return "origin/" + branch in map(lambda it: str(it), self.repo.references)

    def is_merged(self, branch, main):
        merged = self.repo.git.branch('--merged', main)
        return branch in merged

    def branch(self):
        return self.repo.active_branch.name

    def branches(self):
        return self.repo.branches

    def branches_str(self):
        return [x.name for x in self.branches()]

    def checkout(self, branch, new_branch=False):
        try:
            if new_branch:
                return self.repo.git.checkout('-b', branch)
            else:
                return self.repo.git.checkout(branch)
        except git.exc.GitCommandError as e:
            print(e)
            return False

    def work_dir(self):
        return self.repo.working_dir

    def delete_branch(self, branch, hard=False):
        try:
            if hard:
                self.repo.git.branch('-D', branch)
            else:
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

    def fetch(self):
        for remote in self.repo.remotes:
            remote.fetch()

    def compare_hash(self, branch):
        if not self.has_remote(branch):
            return False
        remoteSha = git.Git().execute("git rev-parse origin/" + branch, shell=True, with_stdout=True)
        localSha = git.Git().execute("git rev-parse " + branch, shell=True, with_stdout=True)
        return remoteSha == localSha



