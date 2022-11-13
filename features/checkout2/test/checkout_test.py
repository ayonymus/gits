from unittest import TestCase
from mockito import mock, when, verify, ANY, verifyNoUnwantedInteractions

from features.checkout2.checkout import CheckoutHandler, CheckoutStore
from features.storage.models import Checkout
from tools.githelper import GitHelper


class TestCheckoutHandler(TestCase):

    def setUp(self):
        self.store: CheckoutStore = mock()
        self.git: GitHelper = mock()
        self.time = mock()
        self.handler = CheckoutHandler(self.store, self.git, self.time)

    def test_checkout_git_error(self):
        branch = "new_branch"
        when(self.git).checkout(branch, False).thenReturn(False)

        result = self.handler.checkout(branch)

        self.assertFalse(result)
        verifyNoUnwantedInteractions(self.store)

    def test_checkout_add_new(self):
        branch = "new_branch"
        time = "2022-11-13 18:46:06.093286"

        when(self.git).checkout(branch, False).thenReturn(True)
        when(self.store).load_checkouts().thenReturn(Checkout())
        when(self.time).now().thenReturn(time)

        result = self.handler.checkout(branch)

        expected = Checkout([(branch, time)])

        self.assertTrue(result)

        verify(self.store).load_checkouts()
        verify(self.time).now()
        verify(self.store).store_checkouts(expected)
        verifyNoUnwantedInteractions(self.store)

    def test_checkout_add_new_empty(self):
        branch = "new_branch"
        time = "2022-11-13 18:46:06.093286"

        when(self.git).checkout(branch, False).thenReturn(True)
        when(self.store).load_checkouts().thenReturn(Checkout([]))
        when(self.time).now().thenReturn(time)

        result = self.handler.checkout(branch)

        expected = Checkout([(branch, time)])

        self.assertTrue(result)

        verify(self.store).load_checkouts()
        verify(self.time).now()
        verify(self.store).store_checkouts(expected)
        verifyNoUnwantedInteractions(self.store)

    def test_checkout_add_to_list(self):
        branch = "new_branch"
        time = "2022-11-13 18:46:06.093286"
        branch2 = "new_branch2"
        time2 = "2022-11-13 18:46:06.093286"

        when(self.git).checkout(branch2, False).thenReturn(True)
        when(self.store).load_checkouts().thenReturn(Checkout([(branch, time)]))
        when(self.time).now().thenReturn(time)

        result = self.handler.checkout(branch2)

        expected = Checkout([(branch, time), (branch2, time2)])

        self.assertTrue(result)
        verify(self.store).load_checkouts()
        verify(self.time).now()
        verify(self.store).store_checkouts(expected)
        verifyNoUnwantedInteractions(self.store)

    def test_checkout_dont_add_same_to_list(self):
        branch = "new_branch"
        time = "2022-11-13 18:46:06.093286"
        branch2 = "new_branch"

        when(self.git).checkout(branch2, False).thenReturn(True)
        when(self.store).load_checkouts().thenReturn(Checkout([(branch, time)]))
        when(self.time).now().thenReturn(time)

        result = self.handler.checkout(branch2)

        self.assertTrue(result)
        verify(self.store).load_checkouts()
        verifyNoUnwantedInteractions(self.store)

    def test_checkout_forward_new_branch_flag(self):
        branch = "new_branch"
        time = "2022-11-13 18:46:06.093286"

        when(self.git).checkout(branch, True).thenReturn(True)
        when(self.store).load_checkouts().thenReturn(Checkout())
        when(self.time).now().thenReturn(time)

        result = self.handler.checkout(branch, True)

        expected = Checkout([(branch, time)])

        self.assertTrue(result)

        verify(self.store).load_checkouts()
        verify(self.time).now()
        verify(self.store).store_checkouts(expected)
        verify(self.git).checkout(branch, True)
        verifyNoUnwantedInteractions(self.store)

