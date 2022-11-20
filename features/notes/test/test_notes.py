from datetime import datetime
from unittest import TestCase

from mockito import mock, when, verify, verifyNoUnwantedInteractions

from data.models import Notes, Note, StorageModel
from data.store import Storage2
from features.notes.notes_handler import NotesStore, NotesHandler
from tools.githelper import GitHelper

BRANCH = "branch"
BRANCH2 = "branch2"
TEXT = "Some note"
TEXT2 = "Some note"
TIME = "2022-11-19 21:28:22.606411"
NOTE = Note(TEXT, BRANCH, TIME)
NOTE2 = Note(TEXT2, BRANCH, TIME)
NOTE3 = Note(TEXT2, BRANCH2, TIME)
NOTE_A = Note(TEXT2, BRANCH2, TIME, TIME)


class NotesHandlerTest(TestCase):

    def setUp(self):
        self.git: GitHelper = mock()
        self.store: NotesStore = mock()
        self.time: datetime = mock()
        self.handler = NotesHandler(store=self.store, git=self.git, time=self.time)

        when(self.time).now().thenReturn(TIME)
        when(self.git).current_branch().thenReturn(BRANCH)
        when(self.store).load_notes().thenReturn(Notes([]))

    def test_save_note_in_order(self):
        when(self.store).load_notes().thenReturn(Notes([NOTE]))
        self.handler.save_note(NOTE2)

        verify(self.store).store_notes(Notes([NOTE2, NOTE]))

    def test_add_new_note(self):
        br = self.handler.add_new_note(TEXT)
        self.assertEqual(BRANCH, br)
        verify(self.store).store_notes(Notes([Note(TEXT, BRANCH, TIME)]))

    def test_add_new_note_specif_branch(self):
        br = self.handler.add_new_note(TEXT, BRANCH2)
        self.assertEqual(BRANCH2, br)
        verify(self.store).store_notes(Notes([Note(TEXT, BRANCH2, TIME)]))
        verifyNoUnwantedInteractions(self.git)

    def test_get_notes(self):
        when(self.store).load_notes().thenReturn(Notes([NOTE2, NOTE]))
        expected = [NOTE2, NOTE], {NOTE2: 0, NOTE: 1}
        self.assertEqual(expected, self.handler.get_notes())

    def test_get_notes_empty(self):
        when(self.store).load_notes().thenReturn(Notes([]))
        self.assertEqual(([], {}), self.handler.get_notes())

    def test_get_notes_branch(self):
        when(self.store).load_notes().thenReturn(Notes([NOTE3, NOTE2, NOTE]))
        expected = [NOTE2, NOTE], {NOTE3: 0, NOTE2: 1, NOTE: 2}
        self.assertEqual(expected, self.handler.get_notes(branch=BRANCH))

    def test_get_notes_length(self):
        when(self.store).load_notes().thenReturn(Notes([NOTE3, NOTE2, NOTE]))
        expected = [NOTE3, NOTE2], {NOTE3: 0, NOTE2: 1, NOTE: 2}
        self.assertEqual(expected, self.handler.get_notes(length=2))

    def test_get_notes_full(self):
        when(self.store).load_notes().thenReturn(Notes([NOTE3, NOTE2, NOTE]))
        expected = [NOTE3, NOTE2, NOTE], {NOTE3: 0, NOTE2: 1, NOTE: 2}
        self.assertEqual(expected, self.handler.get_notes(length=2, full=True))

    def test_get_notes_grouped(self):
        when(self.store).load_notes().thenReturn(Notes([NOTE2, NOTE3, NOTE]))
        expected = [NOTE2, NOTE, NOTE3], {NOTE2: 0, NOTE3: 1, NOTE: 2}
        self.assertEqual(expected, self.handler.get_notes(group=True))

    def test_get_notes_no_archived(self):
        when(self.store).load_notes().thenReturn(Notes([NOTE3, NOTE2, NOTE, NOTE_A]))
        expected = [NOTE3, NOTE2, NOTE], {NOTE3: 0, NOTE2: 1, NOTE: 2, NOTE_A: 3}
        self.assertEqual(expected, self.handler.get_notes(archived=False))

    def test_get_notes_archived(self):
        when(self.store).load_notes().thenReturn(Notes([NOTE3, NOTE2, NOTE, NOTE_A]))
        expected = [NOTE3, NOTE2, NOTE, NOTE_A], {NOTE3: 0, NOTE2: 1, NOTE: 2, NOTE_A: 3}
        self.assertEqual(expected, self.handler.get_notes(archived=True))

    def test_archive_note(self):
        to_archive = Note(TEXT, BRANCH, TIME)
        archived = Note(TEXT, BRANCH, TIME, TIME)
        when(self.store).load_notes().thenReturn(Notes([NOTE2, to_archive]))

        result = self.handler.archive_note(1)
        self.assertTrue(result)
        verify(self.store).store_notes(Notes([NOTE2, archived]))

    def test_remove_note(self):
        when(self.store).load_notes().thenReturn(Notes([NOTE2, NOTE]))

        result = self.handler.remove(1)
        self.assertTrue(result)
        verify(self.store).store_notes(Notes([NOTE2]))

    def test_move_note(self):
        when(self.store).load_notes().thenReturn(Notes([NOTE3, NOTE2, NOTE, NOTE_A]))
        expected = [NOTE3, NOTE, NOTE_A, NOTE2]

        self.handler.move(1, 3)

        verify(self.store).store_notes(Notes(expected))


class NotesStoreTest(TestCase):

    def setUp(self):
        self.storage: Storage2 = mock()
        self.note_store = NotesStore(self.storage)

    def test_load_notes_empty(self):
        when(self.storage).load_model().thenReturn(StorageModel())

        notes = self.note_store.load_notes()
        self.assertEqual(Notes([]), notes)

    def test_load_notes_content(self):
        when(self.storage).load_model().thenReturn(StorageModel(notes=Notes([NOTE])))

        notes = self.note_store.load_notes()
        self.assertEqual(Notes([NOTE]), notes)
