from cli.tools import confirm, YES
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
        | new | tag | --setmain | set current as main branch | confirm
        |     |     | --setwork       | set current as work branch | |
        |     |     | -i, --important     | set current as important, so that it wont be cleaned up or deleted | update description |
        |     |     | --custom [arg]  | set custom tag for current branch | |
        |     |     | -l, --list  | list tags | |
        |     |     | --show[tag] | list branches with tags. default: all | |
        |     |     | --remove[tag] | completely remove a tag | confirm |
        """
        parser = subparser.add_parser("tags", help="Add special tags to branches")
        parser.add_argument("--setmain", action="store_true", help="Set current branch the main branch")
        parser.add_argument("--setwork", type=str, help="Set current branch the work branch")
        parser.add_argument("-i, --important", type=str, help="Mark current branch as Important (won't be cleared)")

        parser.set_defaults(func=self.handle)

    def handle(self, args):
        if args.setmain:
            result = YES
            if self.tags.is_main_set():
                result = confirm("Are you sure you want to change main branch?")
            if result == YES:
                self.tags.set_main()
            else:
                print("Main branch not updated.")
        else:
            print(args)

