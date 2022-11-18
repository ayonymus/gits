from unittest import TestCase

from mockito import mock, when, ANY

from data.models import Tags
from features.cleanup.cleanup_handler import CleanupHandler, Validation
from features.tags.tags import TagsHandler
from tools.githelper import GitHelper

CURRENT = "current"
BRANCH = "branch"
MAIN = "main"
WORK = "work"
IMP = "important"

TAGS = Tags(
    main=MAIN,
    work=[WORK],
    important=[IMP]
)


class TestCleanupHandler(TestCase):

    def setUp(self):
        self.tags: TagsHandler = mock()
        self.git: GitHelper = mock()
        self.handler = CleanupHandler(tags_handler=self.tags, git=self.git)

        when(self.tags).get_tags().thenReturn(TAGS)
        when(self.git).is_existing_branch(ANY).thenReturn(True)
        when(self.git).is_merged(ANY, ANY).thenReturn(True)
        when(self.git).current_branch().thenReturn(CURRENT)

    def test_OK_to_delete(self):
        self.assertEqual(Validation.OK_TO_DELETE, self.handler.validate_branch(BRANCH))

    def test_not_exist(self):
        when(self.git).is_existing_branch(BRANCH).thenReturn(False)
        self.assertEqual(Validation.NOT_EXIST, self.handler.validate_branch(BRANCH))

    def test_current(self):
        when(self.git).current_branch().thenReturn(BRANCH)
        self.assertEqual(Validation.CURRENT, self.handler.validate_branch(BRANCH))

    def test_main_not_set(self):
        tags = Tags()
        when(self.tags).get_tags().thenReturn(tags)
        self.assertEqual(Validation.MAIN_NOT_SET, self.handler.validate_branch(BRANCH))

    def test_current_main(self):
        self.assertEqual(Validation.MAIN, self.handler.validate_branch(MAIN))

    def test_not_merged_to_main(self):
        when(self.git).is_merged(BRANCH, MAIN).thenReturn(False)
        self.assertEqual(Validation.NOT_MERGED_TO_MAIN, self.handler.validate_branch(BRANCH))

    def test_current_work(self):
        self.assertEqual(Validation.WORK, self.handler.validate_branch(WORK))

    def test_current_work_none(self):
        tags = Tags(main=MAIN)
        when(self.tags).get_tags().thenReturn(tags)
        print(tags.work)
        self.assertEqual(Validation.OK_TO_DELETE, self.handler.validate_branch(WORK))

    def test_important(self):
        self.assertEqual(Validation.IMPORTANT, self.handler.validate_branch(IMP))

    def test_important_none(self):
        tags = Tags(main=MAIN)
        when(self.tags).get_tags().thenReturn(tags)
        print(tags.work)
        self.assertEqual(Validation.OK_TO_DELETE, self.handler.validate_branch(IMP))

