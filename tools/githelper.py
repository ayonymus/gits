import git
from git import Repo
import os
import re


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
            print('Script should be started from the root directory of a git repository. Exit')
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

    def current_branch(self):
        return self.repo.active_branch.name

    def branches(self):
        return self.repo.branches

    def branches_str(self):
        return [x.name for x in self.branches()]

    def remote_branches(self):
        branches = self.repo.git.branch('--remote', '--sort=-committerdate')  # .strip('*origin/').split('\n')
        branches = re.sub(r'\s*origin/HEAD.*', '', branches)
        return list(filter(None, re.split(r'\s*origin/', branches)))

    def remotes(self):
        return self.repo.remotes

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

    def delete_remote(self, branch):
        try:
            git.Git().execute("git push origin -d " + branch, shell=True, with_stdout=True)
        except git.exc.GitCommandError as e:
            print(e.stderr)
            return False

    def fetch(self):
        for remote in self.repo.remotes:
            remote.fetch(prune=True)

    def is_pushed(self, branch):
        if not self.has_remote(branch):
            return False
        remoteSha = git.Git().execute("git rev-parse origin/" + branch, shell=True, with_stdout=True)
        localSha = git.Git().execute("git rev-parse " + branch, shell=True, with_stdout=True)
        return remoteSha == localSha

    def get_origin_url(self):
        return self.repo.remotes.origin.url


def main():
    gith = GitHelper()
    print(gith.get_origin_url())


if __name__ == '__main__':
    main()
