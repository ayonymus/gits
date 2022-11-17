from termcolor import colored

from cli.tools import YES, confirm
from features.storage.models import Tags
from features.tags.color import Main, Work, Important, Current
from features.tags.tags import TagsHandler


class TagsCli:

    def __init__(self, tags: TagsHandler):
        self.tags = tags

    def add_subparser(self, subparser):
        parser = subparser.add_parser("tags", help="Manage special and custom tags for branches")
        parser.add_argument("--setmain", action="store_true",
                            help=f"Set {Current} branch the {Main} branch")
        parser.add_argument("--setwork", action="store_true",
                            help=f"Set {Current} branch the {Work} branch")
        parser.add_argument("-l", "--worklogs", action="store_true", help=f"Show {Work} branch logs")
        parser.add_argument("-i", "--important", action="store_true",
                            help=f"Mark {Current} branch as {Important} (won't be cleared)")

        parser.set_defaults(func=self.handle)

    def handle(self, args):
        if args.setmain:
            self.set_main()
        elif args.setwork:
            self.tags.set_work()
        elif args.important:
            self.tags.add_important()
        elif args.worklogs:
            self.print_work_logs()
        else:
            self.print_tags()

    def set_main(self):
        result = YES
        if self.tags.is_main_set():
            result = confirm(f"Are you sure you want to change {Main} branch?")
        if result == YES:
            self.tags.set_main()
        else:
            print(f"{Main} branch not updated.")

    def print_tags(self):
        tags: Tags = self.tags.get_tags()
        not_set = "[Not set]"
        print(f"{Main}: {tags.main or not_set}")
        print(f"{Work}: {tags.work[0] if tags.work else not_set or not_set}")
        print(f"{Important}: {tags.important or not_set}")

    def print_work_logs(self):
        tags: Tags = self.tags.get_tags()
        print(f"Most recent {Work} branches")
        print(tags.work)
