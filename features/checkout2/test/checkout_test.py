from unittest import TestCase
from mockito import mock, when, verify, ANY, verifyNoUnwantedInteractions

from features.checkout2.checkout import CheckoutHandler, CheckoutStore
from features.storage.models import Checkout, Tags
from features.tags.tags import TagsHandler
from tools.githelper import GitHelper


class TestCheckoutHandler(TestCase):

    def setUp(self):
        self.store: CheckoutStore = mock()
        self.git: GitHelper = mock()
        self.time = mock()
        self.tags: TagsHandler = mock()
        self.handler = CheckoutHandler(self.store, self.git, self.tags, self.time)

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

    def test_checkout_suffix(self):
        branch = "branch"
        branch_suffixed = branch + '_' + 'fuuu'
        time = "2022-11-13 18:46:06.093286"

        when(self.git).checkout(branch_suffixed, True).thenReturn(True)
        when(self.git).current_branch().thenReturn(branch)
        when(self.store).load_checkouts().thenReturn(Checkout())
        when(self.time).now().thenReturn(time)

        result = self.handler.checkout_suffix('fuuu')

        expected = Checkout([(branch_suffixed, time)])

        self.assertTrue(result)
        verify(self.store).load_checkouts()
        verify(self.time).now()
        verify(self.store).store_checkouts(expected)
        verify(self.git).checkout(branch_suffixed, True)
        verifyNoUnwantedInteractions(self.store)

    def test_get_empty(self):

        checkout = Checkout()
        when(self.store).load_checkouts().thenReturn(checkout)
        when(self.git).branches_str().thenReturn([])
        result = self.handler.get_logs(10, True)

        expected = ([])

        self.assertEqual(expected, result)
        verify(self.store).load_checkouts()
        verifyNoUnwantedInteractions(self.store)
        verifyNoUnwantedInteractions(self.git)

    def test_get_logs(self):
        branch = "branch"
        branch2 = "branch2"
        time = "2022-11-13 18:46:06.093286"
        checkout = Checkout([(branch, time), (branch2, time)])
        when(self.store).load_checkouts().thenReturn(checkout)
        when(self.git).branches_str().thenReturn([branch, branch2])
        result = self.handler.get_logs(10, True)

        expected = ([(branch2, time, False), (branch, time, False)])

        self.assertEqual(expected, result)
        verify(self.store).load_checkouts()
        verifyNoUnwantedInteractions(self.store)
        verifyNoUnwantedInteractions(self.git)

    def test_get_logs_truncated(self):
        branch = "branch"
        branch2 = "branch2"
        branch3 = "branch3"
        branch4 = "branch4"
        time = "2022-11-13 18:46:06.093286"
        checkout = Checkout([(branch, time), (branch2, time), (branch3, time), (branch4, time)])
        when(self.store).load_checkouts().thenReturn(checkout)
        when(self.git).branches_str().thenReturn([branch, branch2])

        result = self.handler.get_logs(2, False)

        expected = ([(branch4, time, True), (branch3, time, True)])

        self.assertEqual(expected, result)
        verify(self.store).load_checkouts()
        verifyNoUnwantedInteractions(self.store)
        verifyNoUnwantedInteractions(self.git)

    def test_checkout_main(self):
        main = "main"
        time = "2022-11-13 18:46:06.093286"

        when(self.git).checkout(main, False).thenReturn(True)
        when(self.store).load_checkouts().thenReturn(Checkout())
        when(self.time).now().thenReturn(time)
        when(self.tags).get_tags().thenReturn(Tags("main"))

        result = self.handler.checkout_main()

        expected = Checkout([(main, time)])

        self.assertEquals(main, result)
        verify(self.store).load_checkouts()
        verify(self.time).now()
        verify(self.store).store_checkouts(expected)
        verifyNoUnwantedInteractions(self.store)

    def test_checkout_main_not_set(self):
        when(self.tags).get_tags().thenReturn(Tags())

        result = self.handler.checkout_main()

        self.assertEquals(None, result)
        verifyNoUnwantedInteractions(self.git)
        verifyNoUnwantedInteractions(self.time)
        verifyNoUnwantedInteractions(self.store)

    def test_checkout_work(self):
        work = "work"
        time = "2022-11-13 18:46:06.093286"

        when(self.git).checkout(work, False).thenReturn(True)
        when(self.store).load_checkouts().thenReturn(Checkout())
        when(self.time).now().thenReturn(time)
        when(self.tags).get_tags().thenReturn(Tags("main", ["work"]))

        result = self.handler.checkout_work()

        expected = Checkout([(work, time)])

        self.assertEquals(work, result)
        verify(self.store).load_checkouts()
        verify(self.time).now()
        verify(self.store).store_checkouts(expected)
        verifyNoUnwantedInteractions(self.store)

    def test_checkout_work_not_set(self):
        when(self.tags).get_tags().thenReturn(Tags())

        result = self.handler.checkout_work()

        self.assertEquals(None, result)
        verifyNoUnwantedInteractions(self.git)
        verifyNoUnwantedInteractions(self.time)
        verifyNoUnwantedInteractions(self.store)
