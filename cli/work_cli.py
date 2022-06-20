
from colorama import Fore, Back, Style


class WorkCli:

    def __init__(self, git, workbranch):
        self.workbranch = workbranch
        self.git = git

    def add_subparser(self, subparsers):
        work_parser = subparsers.add_parser('work', help="Keep track of a currently important branch")
        work_parser.add_argument("-b", action="store_true", help="List branches")
        work_parser.add_argument("current", nargs="?", type=str, default=None, help="Show current work branch")
        work_parser.add_argument("-s", action="store_true", help="Set current work branch")
        work_parser.add_argument("-c", action="store_true", help="Checkout current work branch")
        work_parser.add_argument("-ch", type=int,  help="Checkout work branch from history by id")
        work_parser.add_argument("-H", "--history", action="store_true", help="Show work branch history")
        work_parser.set_defaults(func=self.handle_work)

    def handle_work(self, args):
        if args.s:
            self.set_work_branch()
        elif args.b:
            self.print_branches()
        elif args.c:
            self.checkout_work_branch()
        elif args.ch:
            self.checkout_work_branch_history(args.ch)
        elif args.history:
            self.print_work_branch_history(args.history)
        else:
            self.print_current_work_branch()

    def print_branches(self):
        wrk = str(self.workbranch.get_work_branch())
        br = str(self.git.branch())
        for i, branch in enumerate(self.git.branches()):
            color = Style.DIM
            if str(branch) in self.workbranch.get_work_branch_history():
                color = Fore.WHITE
            if str(branch) == wrk:
                color = Fore.CYAN
            if str(branch) == br:
                color = Fore.GREEN
            print(color + str(branch) + Style.RESET_ALL)


    def print_current_work_branch(self):
        current = self.workbranch.get_work_branch()
        cur = ("not set" if current is None else current)
        print("Current work branch is " + Fore.CYAN + cur + Style.RESET_ALL)

    def print_work_branch_history(self, index):
        cur = self.git.branch()
        cur_found = False
        for i, branch in enumerate(self.workbranch.get_work_branch_history()):
            stat = ""
            color = Fore.WHITE
            if branch == self.workbranch.get_work_branch():
                stat += Fore.CYAN + " (work)"
                color = Fore.CYAN
            if branch == cur:
                stat += Fore.GREEN + " (checked out)"
                color = Fore.GREEN
                cur_found = True
            print(color + str(i) + " " + branch + stat + Style.RESET_ALL)
        if not cur_found:
            print("Current branch: " + Fore.GREEN + branch + Style.RESET_ALL)


    def set_work_branch(self):
        branch = self.workbranch.set_work_branch()
        print("Current work branch is %s" % branch)

    def checkout_work_branch(self):
        branch = self.workbranch.checkout_work_branch()
        print("Switched to branch '%s'" % branch)

    def checkout_work_branch_history(self, index):
        branch = self.workbranch.checkout_work_branch_from_history(index)
        print("No such branch" if branch is None else "Switched to branch '%s'" % branch)
