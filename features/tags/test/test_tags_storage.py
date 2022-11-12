import unittest
from unittest.mock import Mock

from features.tags.tags_storage import TagsStorage, KEY_TAGS, KEY_SPECIAL


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.storage = Mock()
        self.tags = TagsStorage(storage=self.storage)

    def test_store_special_branch(self):
        self.storage.load.return_value = dict()
        self.tags.set_special("main", "branch")

        data = {KEY_TAGS: {KEY_SPECIAL: {"main": "branch"}}}

        self.storage.store.assert_called_with(data)

    def test_get_special_branch(self):
        self.storage.load.return_value = {KEY_TAGS: {KEY_SPECIAL: {"main": "branch"}}}

        self.assertEqual(self.tags.get_special("main"), "branch")
        self.storage.load.assert_called_with()

    def test_get_special_branch_empty(self):
        self.storage.load.return_value = {}

        self.assertEqual(self.tags.get_special("main"), None)
        self.storage.load.assert_called_with()

if __name__ == '__main__':
    unittest.main()
