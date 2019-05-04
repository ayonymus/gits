import unittest
from unittest import TestCase
from unittest.mock import Mock

from tools.checkout import CheckoutHistory

ONE = 'one'
TWO = 'two'
THREE = 'three'


class TestCheckoutHistory(TestCase):

    def setUp(self):
        self.storage = Mock()
        self.git = Mock()
        self.checkout = CheckoutHistory(storage=self.storage, git=self.git)

    def test_checkout_store_branch(self):
        self.storage.load_checkout_history.return_value = []

        self.checkout.checkout(ONE)

        self.git.checkout.assert_called_with(ONE)
        self.storage.store_checkout_history.assert_called_with([ONE])

    def test_checkout_not_store_branch_when_last_is_same(self):
        self.storage.load_checkout_history.return_value = [ONE]

        self.checkout.checkout(ONE)

        self.git.checkout.assert_called_with(ONE)
        self.storage.store_checkout_history.assert_not_called()

    def test_checkout_not_store_branch_when_checkout_not_successful(self):
        self.storage.load_checkout_history.return_value = [ONE]
        self.git.checkout.return_value(False)

        self.checkout.checkout(ONE)

        self.storage.store_checkout_history.assert_not_called()


if __name__ == '__main__':
    unittest.main()
