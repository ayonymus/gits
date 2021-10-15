from unittest import TestCase
from unittest.mock import Mock

from features.cleanup import Cleanup
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
        self.storage.load_cleanup_whitelist.return_value = []
        self.tasks.get_tasks.return_value = []

    def test_cleanup_should_return_not_master(self):
        self.git.branch.return_value = BRANCH

        result = self.cleanup.validate_branch(BRANCH)

        self.assertEqual(Cleanup.NOT_MASTER_OR_DEV, result)

    def test_cleanup_should_return_has_open_tasks(self):
        self.git.branch.return_value = Cleanup.BRANCH_MASTER
        self.tasks.get_tasks.return_value = ["hupppp"]

        result = self.cleanup.validate_branch(BRANCH)

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

        result = self.cleanup.cleanup(BRANCH)

        self.assertEqual(Cleanup.NOT_EXIST, result)

    def test_cleanup_should_return_error(self):
        self.git.branch.return_value = Cleanup.BRANCH_MASTER
        self.git.delete_branch.return_value = GitHelper.ERROR

        result = self.cleanup.cleanup(BRANCH)

        self.assertEqual(Cleanup.ERROR, result)

    def test_cleanup_should_return_success(self):
        self.git.branch.return_value = Cleanup.BRANCH_MASTER
        self.git.delete_branch.return_value = GitHelper.SUCCESS

        result = self.cleanup.cleanup(BRANCH)

        self.tasks.remove_done_tasks.assert_called_with(BRANCH)
        self.assertEqual(Cleanup.SUCCESS, result)

    def test_add_to_whitelist_should_add(self):
        self.storage.load_cleanup_whitelist.return_value = []

        self.cleanup.add_to_whitelist(BRANCH)

        self.storage.store_cleanup_whitelist.assert_called_with([BRANCH])

    def test_add_to_whitelist_should_not_update(self):
        self.storage.load_cleanup_whitelist.return_value = [BRANCH]

        self.cleanup.add_to_whitelist(BRANCH)

        self.storage.store_cleanup_whitelist.assert_not_called()

    def test_remove_from_whitelist_should_change_nothing(self):
        self.storage.load_cleanup_whitelist.return_value = []

        self.cleanup.remove_from_whitelist(BRANCH)

        self.storage.store_cleanup_whitelist.assert_not_called()

    def test_remove_from_whitelist(self):
        self.storage.load_cleanup_whitelist.return_value = [BRANCH]

        self.cleanup.remove_from_whitelist(BRANCH)

        self.storage.store_cleanup_whitelist.assert_called_with([])

    def test_cleanup_should_return_barnch_ignored(self):
        self.git.branch.return_value = Cleanup.BRANCH_MASTER
        self.storage.load_cleanup_whitelist.return_value = [BRANCH]

        result = self.cleanup.validate_branch(BRANCH)

        self.assertEqual(Cleanup.BRANCH_IGNORED, result)
