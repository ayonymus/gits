from unittest import TestCase
from unittest.mock import Mock

from tools.cleanup import Cleanup
from tools.githelper import GitHelper

ONE = "one"
BRANCH = "branch"


class TestCleanup(TestCase):

    def setUp(self):
        self.storage = Mock()
        self.git = Mock()
        self.workbranch = Mock()
        self.tasks = Mock()
        self.cleanup = Cleanup(self.git, self.storage, self.workbranch, self.tasks)

    def test_cleanup_should_return_not_master(self):
        self.git.branch.return_value = BRANCH

        result = self.cleanup.cleanup(BRANCH)

        self.assertEqual(Cleanup.NOT_MASTER_OR_DEV, result)

    def test_cleanup_should_return_has_open_tasks(self):
        self.git.branch.return_value = Cleanup.BRANCH_MASTER
        self.tasks.get_tasks.return_value = ["hupppp"]

        result = self.cleanup.cleanup(BRANCH)

        self.assertEqual(Cleanup.HAS_OPEN_TASKS, result)

    def test_cleanup_should_return_not_merged(self):
        self.git.branch.return_value = Cleanup.BRANCH_MASTER
        self.git.delete_branch.return_value = GitHelper.NOT_MERGED
        self.tasks.get_tasks.return_value = []

        result = self.cleanup.cleanup(BRANCH)

        self.assertEqual(Cleanup.NOT_MERGED, result)

    def test_cleanup_should_return_not_exist(self):
        self.git.branch.return_value = Cleanup.BRANCH_MASTER
        self.git.delete_branch.return_value = GitHelper.NOT_FOUND
        self.tasks.get_tasks.return_value = []

        result = self.cleanup.cleanup(BRANCH)

        self.assertEqual(Cleanup.NOT_EXIST, result)

    def test_cleanup_should_return_error(self):
        self.git.branch.return_value = Cleanup.BRANCH_MASTER
        self.git.delete_branch.return_value = GitHelper.ERROR
        self.tasks.get_tasks.return_value = []

        result = self.cleanup.cleanup(BRANCH)

        self.assertEqual(Cleanup.ERROR, result)

    def test_cleanup_should_return_success(self):
        self.git.branch.return_value = Cleanup.BRANCH_MASTER
        self.git.delete_branch.return_value = GitHelper.SUCCESS
        self.tasks.get_tasks.return_value = []

        result = self.cleanup.cleanup(BRANCH)

        self.assertEqual(Cleanup.SUCCESS, result)
