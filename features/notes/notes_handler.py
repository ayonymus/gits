from datetime import datetime

from mdutils import MdUtils

from data.models import Notes, Note
from data.store import Storage2
from tools.githelper import GitHelper


class NotesStore:
    def __init__(self, store: Storage2):
        self.store = store

    def load_notes(self) -> Notes:
        notes = self.store.load_model().notes
        if notes is None:
            notes = Notes([])
        return notes

    def store_notes(self, notes: Notes):
        data = self.store.load_model()
        data.notes = notes
        self.store.store_model(data)


class NotesHandler:

    def __init__(self, store: NotesStore,  git: GitHelper, time=datetime):
        self.store = store
        self.git = git
        self.time = time

    def add_new_note(self, text: str, branch=None):
        if branch is None:
            branch = self.git.current_branch()
        self.save_note(Note(text=text, branch=branch, created_at=self.time.now()))
        return branch

    def save_note(self, note: Note):
        notes = self.store.load_notes()
        notes.notes.insert(0, note)
        self.store.store_notes(notes)

    def archive_note(self, note_idx):
        notes = self.store.load_notes()
        if note_idx >= len(notes.notes):
            return False
        else:
            note = notes.notes[note_idx]
            note.archived_at = self.time.now()
            self.store.store_notes(notes)
            return True

    def get_notes(self, length=10, full=False, branch=None, group=False, archived=False) -> []:
        notes = self.store.load_notes().notes
        note_ids = {}
        for idx, note in enumerate(notes):
            note_ids[note] = idx
        if not full:
            notes = notes[:length]
        if not archived:
            notes = [note for note in notes if note.archived_at is None]

        if group:
            groups = {}
            for note in notes:
                if note.branch not in groups.keys():
                    groups[note.branch] = [note]
                else:
                    groups[note.branch].append(note)
            notes = []
            for key in groups.keys():
                for note in groups[key]:
                    notes.append(note)
        elif branch is not None:
            notes = [note for note in notes if note.branch == branch]
        return notes, note_ids

    def move(self, start, end):
        data = self.store.load_notes()
        if start >= len(data.notes) or end >= len(data.notes) or start == end:
            return False
        else:
            note = data.notes.pop(start)
            data.notes.insert(end, note)
            self.store.store_notes(data)
            return True

    def remove(self, idx):
        notes = self.store.load_notes()
        if idx >= len(notes.notes):
            return False
        else:
            notes.notes.pop(idx)
            self.store.store_notes(notes)
            return True

    def export_to_markdown(self):
        mdFile = MdUtils(file_name='GitsNotesExported.md', title='Gits: Notes')
        mdFile.new_header(level=1, title='Overview')
        mdFile.new_line(f'Exported at {datetime.now().isoformat("-")}')
        notes, idx = self.get_notes(full=True, archived=True, group=True)

        current_group = None
        archived = []
        for note in notes:
            if note.branch != current_group:
                current_group = note.branch
                # write archived
                if archived:
                    mdFile.new_header(level=3, title="Archived")
                    for arc in archived:
                        mdFile.new_line(arc)
                    archived = []

                # new group
                mdFile.new_header(level=2, title=current_group)
            if note.archived_at:
                archived.append(note)
            else:
                mdFile.new_line(f'{note.created_at.strftime("%Y-%m-%d, %H:%M:%S")} {note.text}')

        if archived:
            mdFile.new_header(level=3, title="Archived")
            for arc in archived:
                mdFile.new_line(f'{arc.created_at.strftime("%Y-%m-%d, %H:%M:%S")} {arc.text}')
        mdFile.create_md_file()



