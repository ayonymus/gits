
class WorkCli:

    def __init__(self, workbranch):
        self.workbranch = workbranch

    def add_subparser(self, subparsers):
        work_parser = subparsers.add_parser('work', help="Keep track of a currently important branch")
        work_parser.add_argument("current", nargs="?", type=str, default=None, help="Show current work branch")
        work_parser.add_argument("-s", action="store_true", help="Set current work branch")
        work_parser.add_argument("-c", action="store_true", help="Checkout current work branch")
        work_parser.add_argument("-ch", type=int,  help="Checkout work branch from history by id")
        work_parser.add_argument("-H", "--history", action="store_true", help="Show work branch history")
        work_parser.set_defaults(func=self.handle_work)

    def handle_work(self, args):
        if args.s:
            self.set_work_branch()
        elif args.c:
            self.checkout_work_branch()
        elif args.ch:
            self.checkout_work_branch_history(args.W)
        elif args.history:
            self.print_work_branch_history()
        else:
            self.print_current_work_branch()

    def print_current_work_branch(self):
        current = self.workbranch.get_work_branch()
        print("Current work branch is", ("not set" if current is None else current))

    def print_work_branch_history(self):
        for i, branch in enumerate(self.workbranch.get_work_branch_history()):
            print(i, branch)

    def set_work_branch(self):
        branch = self.workbranch.set_work_branch()
        print("Current work branch is %s" % branch)

    def checkout_work_branch(self):
        branch = self.workbranch.checkout_work_branch()
        print("Switched to branch '%s'" % branch)

    def checkout_work_branch_history(self, index):
        branch = self.workbranch.checkout_work_branch_from_history(index)
        print("No such branch" if branch is None else "Switched to branch '%s'" % branch)