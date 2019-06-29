import unittest
from unittest.mock import Mock

from features.taskhandler import TaskHandler

BRANCH = "barbie"
BRANCH2 = "barbie2"
TASK1 = "go go go"
TASK2 = "go go go2"
TASK3 = "go go go3"


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

    def test_get_all_tasks_return_all_tasks(self):
        self.storage.load_all_tasks.return_value = {BRANCH: [TASK1, TASK2]}

        result = self.tasks.get_all_tasks()

        self.assertEqual({BRANCH: [TASK1, TASK2]}, result)

    def test_get_tasks_return_all_branch_tasks(self):
        self.storage.load_all_tasks.return_value = {BRANCH: [TASK1, TASK2]}

        result = self.tasks.get_tasks(BRANCH)

        self.assertEqual([TASK1, TASK2], result)

    def test_get_tasks_returns_empty_list(self):
        self.storage.load_all_tasks.return_value = dict()

        result = self.tasks.get_tasks(BRANCH)

        self.assertEqual([], result)

    def test_remove_task_should_return_true(self):
        self.storage.load_all_tasks.return_value = {BRANCH: [TASK1, TASK2]}

        result = self.tasks.remove_task(BRANCH, 0)

        self.storage.store_tasks.assert_called_with({BRANCH: [TASK2]})
        self.assertTrue(result)

    def test_remove_task_should_return_false_when_wrong_index(self):
        self.storage.load_all_tasks.return_value = {BRANCH: [TASK1, TASK2]}

        result = self.tasks.remove_task(BRANCH, 20)

        self.storage.store_tasks.assert_not_called()
        self.assertFalse(result)

    def test_remove_task_should_return_false_when_wrong_branch(self):
        self.storage.load_all_tasks.return_value = {BRANCH: [TASK1, TASK2]}

        result = self.tasks.remove_task(BRANCH2, 0)

        self.storage.store_tasks.assert_not_called()
        self.assertFalse(result)

    def test_get_done_tasks_returns_empty_list(self):
        self.storage.load_all_done_tasks.return_value = dict()

        result = self.tasks.get_done_tasks(BRANCH)

        self.assertEqual([], result)

    def test_get_done_tasks_return_all_branch_tasks(self):
        self.storage.load_all_done_tasks.return_value = {BRANCH: [TASK1, TASK2]}

        result = self.tasks.get_done_tasks(BRANCH)

        self.assertEqual([TASK1, TASK2], result)

    def test_set_task_done_should_return_false_when_wrong_index(self):
        self.storage.load_all_tasks.return_value = {BRANCH: [TASK1, TASK2]}
        self.storage.load_all_done_tasks.return_value = {}

        result = self.tasks.set_task_done(BRANCH, 10)

        self.assertFalse(result)
        self.storage.store_tasks.assert_not_called()
        self.storage.store_done_tasks.assert_not_called()

    def test_set_task_done_should_return_true_when_index_exists(self):
        self.storage.load_all_tasks.return_value = {BRANCH: [TASK1, TASK2]}
        self.storage.load_all_done_tasks.return_value = {}

        result = self.tasks.set_task_done(BRANCH, 1)

        self.assertTrue(result)
        #self.storage.store_tasks.assert_called_with({BRANCH: [TASK1]})
        self.storage.store_done_tasks.assert_called_with({BRANCH: [TASK2]})

    def test_remove_done_tasks(self):
        self.storage.load_all_done_tasks.return_value = {BRANCH: [TASK1, TASK2]}

        self.tasks.remove_done_tasks(BRANCH)

        self.storage.store_done_tasks.assert_called_with({})

    def test_move_task_should_return_false_when_wrong_index(self):
        self.storage.load_all_tasks.return_value = {BRANCH: [TASK1, TASK2]}

        result = self.tasks.move_task(BRANCH, 10, 0)

        self.assertFalse(result)
        self.storage.store_tasks.assert_not_called()

        result = self.tasks.move_task(BRANCH, 0, 10)

        self.assertFalse(result)
        self.storage.store_tasks.assert_not_called()

    def test_move_task_should_return_true_when_right_index(self):
        self.storage.load_all_tasks.return_value = {BRANCH: [TASK1, TASK2, TASK3]}

        result = self.tasks.move_task(BRANCH, 2, 0)

        self.storage.store_tasks.assert_called_with({BRANCH: [TASK3, TASK1, TASK2]})
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
