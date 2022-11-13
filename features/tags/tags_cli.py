from cli.tools import confirm, YES
from features.storage.models import Tags
from features.tags.tags import TagsHandler

"""
            Fore.GREEN + "Current" + Fore.RESET,
            Fore.BLUE + "Main" + Fore.RESET,
            Fore.CYAN + "Work" + Fore.RESET,
            Style.DIM + "Not work branch" + Style.RESET_ALL,
            "\x1B[4m" + "Ignore cleanup" + "\x1B[0m") // undewrline
"""


class TagsCli:

    def __init__(self, tags: TagsHandler):
        self.tags = tags

    def add_subparser(self, subparser):
        """
        |     |     | -i, --important     | set current as important, so that it wont be cleaned up or deleted | update description |
        |     |     | -l, --list  | list tags | |
        """
        parser = subparser.add_parser("tags", help="Add special tags to branches")
        parser.add_argument("--setmain", action="store_true", help="Set current branch the main branch")
        parser.add_argument("--setwork", action="store_true", help="Set current branch the work branch")
        parser.add_argument("-l", "--worklogs", action="store_true", help="Show work branch logs")
        parser.add_argument("-i", "--important", action="store_true",
                            help="Mark current branch as Important (won't be cleared)")

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
            result = confirm("Are you sure you want to change main branch?")
        if result == YES:
            self.tags.set_main()
        else:
            print("Main branch not updated.")

    def print_tags(self):
        tags: Tags = self.tags.get_tags()
        print(tags.main)
        print(tags.work)
        print(tags.important)

    def print_work_logs(self):
        tags: Tags = self.tags.get_tags()
        print(tags.work)
