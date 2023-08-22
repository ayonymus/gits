from tabulate import tabulate

from cli.color import deleted, warn
from cli.selector import ListSelector
from cli.tools import confirm, is_valid_index
from features.notes.notes_handler import NotesHandler


class NotesCli:

    def __init__(self, handler: NotesHandler):
        self.handler = handler

    def add_subparser(self, subparsers):
        parser = subparsers.add_parser('note', help="Take notes of your work")
        parser.add_argument("--add", nargs="?", type=str, default=None, help="Add a new note")
        parser.add_argument("-b", "--branch", nargs="?", type=str, default=None,
                            help=f"Specify a branch")
        parser.add_argument("-l", "--logs", nargs='?', const=10, type=int,
                            help="List most recent notes. Provide -f flag for full list.")
        parser.add_argument("-f", "--full", action="store_true", help="Flag to use full notes list.")
        parser.add_argument("-g", "--group",  action="store_true",
                            help="Group by branch")
        parser.add_argument("--archived", action="store_true", help="Flag to show archived notes.")
        parser.add_argument("-a", "--archive", nargs='?', const=-1, type=int, help="Archive a note by idx")
        parser.add_argument("-d", "--delete", nargs='?', const=-1, type=int, help=f"{deleted('Delete')} a note by idx")
        parser.add_argument("-m", "--move", nargs=2, type=int, help="Remove a note by index. idx1: source, idx2 target")
        parser.add_argument("--movetop", nargs=1, type=int, help="Move note to top of list")
        parser.add_argument("-s", "--select", action="store_true",
                            help=f'Select note from list. Combine with -b, -l, -a, -d')
        parser.add_argument("--export", action="store_true", help="Export notes to Notes.md")
        parser.set_defaults(func=self.handle)

    def handle(self, args):
        if args.add:
            branch = self.handler.add_new_note(args.add, args.branch)
            print(f'Note added to {branch}')
        elif args.select:
            self.select(args)
        elif args.archive:
            self.archive(args.archive[0])
        elif args.delete:
            self.delete(args.delete)
        elif args.move:
            self.move(args.move[0], args.move[1])
        elif args.movetop:
            self.move(args.movetop[0], 0)
        elif args.logs:
            self.print_notes(args.logs, args.full, args.branch, args.group, args.archived)
        elif args.export:
            self.handler.export_to_markdown()
        else:
            self.print_notes(args.logs)

    def print_notes(self, length, full=False, branch=None, group=False, archived=False):
        notes, ids = self.handler.get_notes(length, full, branch, group, archived)
        display = []
        for idx, note in enumerate(notes):
            row = [f'[{ids[note]}]', note.created_at.strftime("%Y-%m-%d, %H:%M:%S"), note.branch, note.text]
            if archived:
                row.append(note.archived_at)
            display.append(row)

        headers = ["idx", "date", "branch", "note"]
        if archived:
            headers.append('archived')
        print(tabulate(display, headers=headers))

    def select(self, args):
        note_objects, ids = self.handler.get_notes(args.logs, args.full, args.branch, args.group, args.archived)
        note_str = [note.short_str() for note in note_objects]

        selector = ListSelector(note_str, lambda selected: self.handle_selection(ids[note_objects[selected]], args.archive, args.delete))
        selector.start()

    def handle_selection(self, selected, archive, delete):
        if archive:
            self.archive(selected)
        elif delete:
            self.delete(selected)

    def archive(self, idx):
        notes, ids = self.handler.get_notes()
        if not is_valid_index(notes, idx):
            print("Idx is not valid")
            return

        print(f'{notes[idx].text}')
        result = confirm(f'Are you sure you want to {warn("archive")} this note?')
        if result:
            self.handler.archive_note(idx)
            print("Note archived.")
        else:
            print("Note not archived.")

    def delete(self, idx):
        if idx == -1:
            print("Provide a valid idx")
            return
        notes, ids = self.handler.get_notes(full=True, archived=True)
        if not is_valid_index(notes, idx):
            print("Idx is not valid")
            return

        print(f'{notes[idx].text}')
        result = confirm(f'Are you sure you want to {deleted("remove")} this note?')
        if result:
            self.handler.remove(idx)
            print("Note removed.")
        else:
            print("Note not removed.")

    def move(self, start, end):
        notes, ids = self.handler.get_notes(full=True, archived=True)
        if not is_valid_index(notes, start):
            print("Start idx is not valid")
            return
        if not is_valid_index(notes, end):
            print("End idx is not valid")
            return
        print(f'Moving note "{notes[start]}" to {end}')
        self.handler.move(start, end)
