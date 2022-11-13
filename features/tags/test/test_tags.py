from unittest import TestCase

from mockito import when, ANY, verify
from mockito.mocking import mock

from features.storage.models import Tags
from features.storage.store import Storage2, StorageModel
from features.tags.tags import TagsStorage


class TestTagsStorage(TestCase):

    def setUp(self):
        self.storage: Storage2 = mock()
        self.tags = TagsStorage(storage=self.storage)

    def test_store_tags(self):
        expected = StorageModel(Tags("one", "two", "three"))
        when(self.storage).load_model().thenReturn(expected)

        newtags = Tags("Three", "Four", "Five")
        self.tags.store_tags(newtags)

        verify(self.storage).store_model(StorageModel(Tags("Three", "Four", "Five")))

    def test_load_tags(self):
        expected = StorageModel(Tags("one", "two", "three"))
        when(self.storage).load_model().thenReturn(expected)
        self.assertEqual(expected.tags, self.tags.load_tags())
