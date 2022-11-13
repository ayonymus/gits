from termcolor import colored

from cli.tools import confirm, YES
from features.storage.models import Tags
from features.tags.tags import TagsHandler


Current = colored('Current', 'green')
Main = colored('Main', 'blue')
Work = colored('Work', 'cyan')
Important = "\x1B[4m" + "Important" + "\x1B[0m"


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
            result = confirm("Are you sure you want to change %s branch?" % Main)
        if result == YES:
            self.tags.set_main()
        else:
            print("%s branch not updated." % Main)

    def print_tags(self):
        tags: Tags = self.tags.get_tags()
        print(f"{Main}: {tags.main}")
        print(f"{Work}: {tags.work[0] or None}")
        print(f"{Important}: {tags.important}")

    def print_work_logs(self):
        tags: Tags = self.tags.get_tags()
        print(f"Most recent {Work} branches")
        print(tags.work)
