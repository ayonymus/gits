from cli.color import Work, work, error, Deleted, main, important, apply_color
from features.work.work import WorkHandler


class WorkCli:

    def __init__(self, handler: WorkHandler):
        self.handler = handler

    def add_subparser(self, subparsers):
        parser = subparsers.add_parser('work', help="Keep track of work")
        parser.add_argument("current", nargs="?", type=str, default=None, help=f"Show current {Work} branch")
        parser.add_argument("-s", "--setwork", action="store_true", help=f"Set current branch as {Work} branch") ## in tags
        parser.add_argument("-c", "--checkout", action="store_true", help=f"Checkout current {Work} branch")     ## in checkout
        parser.add_argument("-l", "--logs", nargs='?', const=10, type=int,
                                 help=f"Show truncated {Work} branch logs, most recent first. Provide -f flag for full list.") ## in tags
        parser.add_argument("-f", "--full", action="store_true", help="Use full log list.")
        parser.set_defaults(func=self.handle)

    def handle(self, args):
        if args.setwork:
            self.set_work_branch()
        elif args.checkout:
            self.checkout_work_branch()
        elif args.logs:
            self.show_logs(args.logs, args.full)

    def set_work_branch(self):
        branch = self.handler.set_work()
        print(f"Current work branch is now {work(branch)}")

    def checkout_work_branch(self):
        branch = self.handler.checkout_work_branch()
        if branch is not None:
            print(f"Switched to branch '{work(branch)}'")
        else:
            print(f"'{error('Could not')} checkout to branch '{branch}'")

    def show_logs(self, length, full):
        tags = self.handler.tags.get_tags()
        logs = self.handler.get_logs(length, full)
        for log in logs:
            print(f'{apply_color(log[0], tags, log[1])} {Deleted if log[1] else ""}')

