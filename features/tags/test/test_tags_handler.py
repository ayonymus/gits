from unittest import TestCase

from mockito import mock, when, verify

from features.storage.models import Tags
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

