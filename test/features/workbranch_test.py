import unittest
from unittest.mock import Mock

from features.workbranch import Workbranch

ONE = 'one'
TWO = 'two'
THREE = 'three'


class TestWorkBranchMethods(unittest.TestCase):

    def setUp(self):
        self.storage = Mock()
        self.git = Mock()
        self.checkout = Mock()
        self.wb = Workbranch(self.storage, self.checkout, self.git)

    def test_current_work_branch_should_be_None(self):
        self.storage.load_work_branches.return_value = []
        self.assertIsNone(self.wb.get_work_branch())

    def test_current_work_branch_is_last_in_history(self):
        self.storage.load_work_branches.return_value = [ONE, TWO]
        self.assertEqual(TWO, self.wb.get_work_branch())

    def test_work_branch_history(self):
        self.storage.load_work_branches.return_value = [ONE, TWO]
        self.assertEqual([ONE, TWO], self.wb.get_work_branch_history())

    def test_set_current_work_branch_when_history_empty(self):
        # given
        self.storage.load_work_branches.return_value = []
        self.git.branch.return_value = THREE
        # when
        result = self.wb.set_work_branch()
        # then
        self.assertEqual(THREE, result)
        self.storage.update_branch_history.assert_called_with([THREE])

    def test_set_current_work_branch(self):
        # given
        self.storage.load_work_branches.return_value = [ONE, TWO]
        self.git.branch.return_value = THREE
        # when
        result = self.wb.set_work_branch()
        # then
        self.assertEqual(THREE, result)
        self.storage.update_branch_history.assert_called_with([ONE, TWO, THREE])

    def test_do_not_set_current_work_branch_when_same_as_last(self):
        # given
        self.storage.load_work_branches.return_value = [ONE, TWO]
        self.git.branch.return_value = TWO
        # when
        result = self.wb.set_work_branch()
        # then
        self.assertEqual(TWO, result)
        self.storage.update_branch_history.assert_not_called()

    def test_do_not_checkout_work_branch_when_not_set(self):
        # given
        self.storage.load_work_branches.return_value = []
        # when
        result = self.wb.checkout_work_branch()
        # then
        self.assertEqual(None, result)
        self.checkout.checkout.assert_not_called()

    def test_checkout_work_branch(self):
        # given
        self.storage.load_work_branches.return_value = [ONE]
        # when
        result = self.wb.checkout_work_branch()
        # then
        self.assertEqual(ONE, result)
        self.checkout.checkout.assert_called_with(ONE)

    def test_do_not_checkout_work_branch_from_history_when_no_history(self):
        # given
        self.storage.load_work_branches.return_value = []
        # when
        result = self.wb.checkout_work_branch_from_history(1)
        # then
        self.assertEqual(None, result)
        self.checkout.checkout.assert_not_called()

    def test_do_not_checkout_work_branch_from_history_when_history_short(self):
        # given
        self.storage.load_work_branches.return_value = [ONE]
        # when
        result = self.wb.checkout_work_branch_from_history(1)
        # then
        self.assertEqual(None, result)
        self.checkout.checkout.assert_not_called()

    def test_checkout_work_branch_from_history(self):
        # given
        self.storage.load_work_branches.return_value = [ONE]
        # when
        result = self.wb.checkout_work_branch_from_history(0)
        # then
        self.assertEqual(ONE, result)
        self.checkout.checkout.assert_called_with(ONE)


if __name__ == '__main__':
    unittest.main()
