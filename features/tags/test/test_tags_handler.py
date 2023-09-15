from unittest import TestCase

from mockito import mock, when, verify

from data.models import Tags
from features.tags.tags import TagsStorage, TagsHandler
from tools.githelper import GitHelper


class TestTagHandler(TestCase):

    def setUp(self):
        self.store: TagsStorage = mock()
        self.git: GitHelper = mock()
        self.handler = TagsHandler(store=self.store, git=self.git)

    def test_is_main_set_true(self):
        expected = Tags("one", "two", "three")
        when(self.store).load_tags().thenReturn(expected)

        self.assertTrue(self.handler.is_main_set())

    def test_is_main_set_false(self):
        expected = Tags(None, "two", "three")
        when(self.store).load_tags().thenReturn(expected)

        self.assertFalse(self.handler.is_main_set())

    def test_set_main(self):
        expected = Tags(None, "two", "three")
        when(self.store).load_tags().thenReturn(expected)
        when(self.git).current_branch().thenReturn("one")

        self.handler.set_main()

        verify(self.store).store_tags(Tags("one", "two", "three"))

    def test_set_work(self):
        expected = Tags("one", None, {"three"})
        when(self.store).load_tags().thenReturn(expected)
        when(self.git).current_branch().thenReturn("two")

        self.handler.set_work()

        verify(self.store).store_tags(Tags("one", ["two"], {"three"}))

    def test_set_work_after_unset(self):
        expected = Tags("one", [None, "four"], {"three"})
        when(self.store).load_tags().thenReturn(expected)
        when(self.git).current_branch().thenReturn("two")

        self.handler.set_work()

        verify(self.store).store_tags(Tags("one", ["two", "four"], {"three"}))

    def test_set_work_existing(self):
        expected = Tags("one", ["two"], {"three"})
        when(self.store).load_tags().thenReturn(expected)
        when(self.git).current_branch().thenReturn("four")

        self.handler.set_work()

        verify(self.store).store_tags(Tags("one", ["four", "two"], {"three"}))

    def test_set_work_not_same(self):
        expected = Tags("one", ["four", "two"], {"three"})
        when(self.store).load_tags().thenReturn(expected)
        when(self.git).current_branch().thenReturn("four")

        self.handler.set_work()

        verify(self.store).store_tags(Tags("one", ["four", "two"], {"three"}))

    def test_add_important(self):
        expected = Tags("one", ["two"], None)
        when(self.store).load_tags().thenReturn(expected)
        when(self.git).current_branch().thenReturn("three")

        self.handler.add_important()

        verify(self.store).store_tags(Tags("one", ["two"], {"three"}))

    def test_add_important_already_existing_dict(self):
        expected = Tags("one", "two",  {"three"})
        when(self.store).load_tags().thenReturn(expected)
        when(self.git).current_branch().thenReturn("four")

        self.handler.add_important()

        verify(self.store).store_tags(Tags("one", "two", {"three", "four"}))

    def test_add_important_already_in(self):
        expected = Tags("one", "two",  {"three"})
        when(self.store).load_tags().thenReturn(expected)
        when(self.git).current_branch().thenReturn("three")

        self.handler.add_important()

        verify(self.store).store_tags(Tags("one", "two", {"three"}))

    def test_unset_important(self):
        expected = Tags("one", "two",  {"three", "four"})
        when(self.store).load_tags().thenReturn(expected)
        when(self.git).current_branch().thenReturn("four")

        self.handler.unset()

        verify(self.store).store_tags(Tags("one", "two", {"three"}))

    def test_unset_work(self):
        expected = Tags("one", ["two"],  {"three", "four"})
        when(self.store).load_tags().thenReturn(expected)
        when(self.git).current_branch().thenReturn("two")

        self.handler.unset()

        verify(self.store).store_tags(Tags("one", [None, "two"], {"three", "four"}))
