import unittest
from unittest.mock import Mock

from tools.taskhandler import TaskHandler

BRANCH = "barbie"
TASK1 = "go go go"
TASK2 = "go go go"


class TestTasksMethods(unittest.TestCase):

    def setUp(self):
        self.storage = Mock()
        self.tasks = TaskHandler(storage=self.storage)

    def test_store_first_task(self):
        self.storage.load_all_tasks.return_value = dict()

        self.tasks.assign_task(BRANCH, TASK1)

        self.storage.store_tasks.assert_called_with({BRANCH: [TASK1]})

    def test_store_more_task(self):
        self.storage.load_all_tasks.return_value = {BRANCH: [TASK1]}

        self.tasks.assign_task(BRANCH, TASK2)

        self.storage.store_tasks.assert_called_with({BRANCH: [TASK1, TASK2]})

    def test_get_tasks_return_all_branch_tasks(self):
        self.storage.load_all_tasks.return_value = {BRANCH: [TASK1, TASK2]}

        result = self.tasks.get_tasks(BRANCH)

        self.assertEqual([TASK1, TASK2], result)

    def test_get_tasks_return_empty_list(self):
        self.storage.load_all_tasks.return_value = dict()

        result = self.tasks.get_tasks(BRANCH)

        self.assertEqual([], result)


if __name__ == '__main__':
    unittest.main()
