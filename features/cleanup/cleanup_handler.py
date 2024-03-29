from enum import Enum

from features.tags.tags import TagsHandler
from tools.githelper import GitHelper


class Validation(Enum):
    OK_TO_DELETE = 0
    NOT_EXIST = 4
    CURRENT = 6
    NOT_SYNC_WITH_REMOTE = 10
    MAIN_NOT_SET = 20
    MAIN = 21
    NOT_MERGED_TO_MAIN = 22
    WORK = 30
    IMPORTANT = 40


class CleanupHandler:

    def __init__(self, git: GitHelper, tags_handler: TagsHandler):
        self.git = git
        self.tags_handler = tags_handler

    def validate_branch(self, branch) -> Validation:
        tags = self.tags_handler.get_tags()
        if not self.git.is_existing_branch(branch):
            return Validation.NOT_EXIST
        if self.git.current_branch() == branch:
            return Validation.CURRENT
        if self.git.has_remote(branch) and not self.git.is_pushed(branch):
            return Validation.NOT_SYNC_WITH_REMOTE
        if tags.main is None:
            return Validation.MAIN_NOT_SET
        if branch == tags.main:
            return Validation.MAIN
        if not self.git.is_merged(branch, tags.main):
            return Validation.NOT_MERGED_TO_MAIN
        if tags.work is not None and branch == tags.work[0]:
            return Validation.WORK
        if tags.important is not None and branch in tags.important:
            return Validation.IMPORTANT
        return Validation.OK_TO_DELETE

    def delete(self, branch, hard=False):
        result = self.git.delete_branch(branch, hard)
        print(result)
        return result == GitHelper.SUCCESS

    def get_branches(self):
        return self.git.branches_str()

    def has_remote(self, branch):
        return self.git.has_remote(branch)

