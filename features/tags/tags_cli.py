from cli.tools import YES, confirm
from data.models import Tags
from cli.color import Main, Work, Important, Current, work, main_
from features.tags.tags import TagsHandler


class TagsCli:

    def __init__(self, tags: TagsHandler):
        self.parser = None
        self.tags = tags

    def add_subparser(self, subparser):
        self.parser = subparser.add_parser("mark", help="Manage branch markings")
        self.parser.add_argument("-w", "--work", action="store_true",
                                 help=f"Mark {Current} branch the {Work} branch")
        self.parser.add_argument("-i", "--important", action="store_true",
                                 help=f"Mark {Current} branch as {Important} (won't be cleared)")
        self.parser.add_argument("--main", action="store_true",
                                 help=f"Mark {Current} branch the {Main} branch")
        self.parser.add_argument("--unset", action="store_true",
                                 help=f"Unset current branch {Work} or {Important} mark.")
        self.parser.set_defaults(func=self.handle)

    def handle(self, args):
        if args.main:
            self.set_main()
        elif args.unset:
            self.unset()
        elif args.work:
            self.setwork()
        elif args.important:
            self.tags.add_important()
        else:
            self.parser.print_help()

    def set_main(self):
        result = YES
        if self.tags.is_main_set():
            result = confirm(f"Are you sure you want to change {Main} branch?")
        if result == YES:
            self.tags.set_main()
            print(f"{main_(self.tags.get_tags().main)} is now the {Main} branch")
        else:
            print(f"{Main} branch not updated.")

    def print_tags(self):
        tags: Tags = self.tags.get_tags()
        not_set = "[Not set]"
        print(f"{Main}: {tags.main or not_set}")
        print(f"{Work}: {tags.work[0] if tags.work and tags.work[0] is not None else not_set}")
        print(f"{Important}: {tags.important or not_set}")

    def unset(self):
        self.tags.unset()
        print("Current branch is not marked any more.")

    def setwork(self):
        self.tags.set_work()
        print(f"{work(self.tags.get_tags().work[0])} is now the {Work} branch")
