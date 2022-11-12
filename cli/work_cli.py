from colorama import Fore, Style

WORK = Fore.CYAN + "work" + Style.RESET_ALL


class WorkCli:

    def __init__(self, git, workbranch):
        self.workbranch = workbranch
        self.git = git

    def add_subparser(self, subparsers):
        work_parser = subparsers.add_parser('work', help="Keep track of an important branch")
        work_parser.add_argument("current", nargs="?", type=str, default=None, help="Show current " + WORK + " branch")
        work_parser.add_argument("-s", action="store_true", help="Set current branch as " + WORK + " branch")
        work_parser.add_argument("-c", action="store_true", help="Checkout current " + WORK + " branch")
        work_parser.add_argument("-ch", type=int, help="Checkout " + WORK + " branch from work history by idx")
        work_parser.add_argument("-H", "--history", nargs='?', const=10, type=int,
                                 help="Show " + WORK + " branch history, most recent first. Default 10, 0 show full list")
        work_parser.add_argument("--unset", action="store_true", help="Unset " + WORK + " branch")
        work_parser.set_defaults(func=self.__handle_work__)

    def __handle_work__(self, args):
        if args.s:
            self.set_work_branch()
        elif args.c:
            self.checkout_work_branch()
        elif args.ch:
            self.checkout_work_branch_history(args.ch)
        elif args.history is not None:
            self.print_work_branch_history(args.history)
        elif args.unset:
            self.unset_work_branch()
        else:
            self.print_current_work_branch()

    def print_current_work_branch(self):
        current = self.workbranch.get_work_branch()
        cur = ("not set" if current is None else current)
        print("Current work branch is " + Fore.CYAN + cur + Style.RESET_ALL)

    def print_work_branch_history(self, length):
        current_br = self.git.current_branch()
        wrk = str(self.workbranch.get_work_branch())
        current_local_branches = self.git.branches_str()

        history = self.workbranch.get_work_branch_history()
        if length != 0:
            history = history[:length]

        for i, branch in enumerate(history):
            br = str(branch)
            color = ""
            if br in self.workbranch.get_work_branch_history():
                color = Fore.WHITE
            if br == wrk:
                color = Fore.CYAN
            if current_br == branch:
                color = Fore.GREEN
            if branch not in current_local_branches:
                color = Fore.LIGHTRED_EX + Style.DIM
            print(color + str(i) + " " + str(branch) + Style.RESET_ALL)

    def set_work_branch(self):
        branch = self.workbranch.set_work_branch()
        print("Current work branch is " + Fore.CYAN + branch + Style.RESET_ALL)

    def checkout_work_branch(self):
        branch, result = self.workbranch.checkout_work_branch()
        if result:
            print("Switched to current work branch: " + Fore.CYAN + branch + Style.RESET_ALL)
        else:
            print("Couldn't switch to work branch: " + Fore.CYAN + branch + Style.RESET_ALL)

    def checkout_work_branch_history(self, index):
        branch, result = self.workbranch.checkout_work_branch_from_history(index)
        if result:
            print("Switched to current work branch: " + Fore.CYAN + branch + Style.RESET_ALL)
        elif branch is None:
            print("No such branch")
        else:
            print("Couldn't switch to work branch: " + Fore.CYAN + branch + Style.RESET_ALL)

    def unset_work_branch(self):
        self.workbranch.unset_work_branch()
        print("No work branch selected")
