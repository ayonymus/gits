
from colorama import Fore, Style

from cli.tools import dedup


class CheckoutCli:

    def __init__(self, git, checkout_history, workbranch, cleanup):
        self.git = git
        self.checkoutHistory = checkout_history
        self.workbranch = workbranch
        self.cleanup = cleanup
        self.full = False

    def add_subparser(self, subparsers):
        checkout_parser = subparsers.add_parser('checkout', help="Keep a history of checked out branches in a more readable way than reflog")
        checkout_parser.add_argument("checkout", nargs="?", type=str, default=None,
                                     help="Check out branch and add to checkout history")
        checkout_parser.add_argument("-a", "--activity", nargs='?', const=10, type=int,
                                    help="Show most recently checked out branches, duplicates removed, most recent first. Default 10, 0 list all")
        checkout_parser.add_argument("-b", "--branch", type=str, default=None,
                                     help="Create new branch, check out, and add to checkout history")
        checkout_parser.add_argument("--suffix", type=str,
                                     help="Create and check out branch with current's name plus a suffix")
        checkout_parser.add_argument("-H", "--history", type=int,
                                     help="Check out a branch from branch history based on id")
        checkout_parser.add_argument("-f", "--full", action="store_true", help="Full branch checkout history with duplicates. Combine with -a and -H")
        checkout_parser.add_argument("-m", "--main", action="store_true", help="Check out main branch")
        checkout_parser.add_argument("-w", "--work", action="store_true", help="Check out work branch")

        checkout_parser.set_defaults(func=self.handle_checkout)

    def handle_checkout(self, args):
        if args.full:
            self.full = True
        if args.checkout is not None:
            self.checkout(args.checkout)
        elif args.activity is not None:
            self.checkout_activity(args.activity)
        elif args.branch:
            self.checkout(args.branch, True)
        elif args.suffix:
            self.checkout("%1s_%2s" % (self.git.branch(), args.suffix), True)
        elif args.history:
            self.checkout_from_history(args.history)
        elif args.main:
            self.checkout_main()
        elif args.work:
            self.checkout_work()
        elif args.example is not None:
            print(args.example)

    def checkout(self, branch, new_branch=False):
        if not new_branch and branch not in self.git.branches():
            self.git.checkout(branch)
            return
        result = self.checkoutHistory.checkout(branch, new_branch)
        if result:
            print("Current branch is \n %s" % branch)
        else:
            print("Could not check out branch")
        return result

    def checkout_activity(self, length):
        wrk = str(self.workbranch.get_work_branch())
        current_br = str(self.git.branch())
        current_local_branches = self.git.branches_str()

        history = self.checkoutHistory.get_checkout_history()
        history.reverse()
        if not self.full:
            history = dedup(history)
        if length != 0:
            history = history[:length]

        for i, branch in enumerate(history):
            br = str(branch)
            color = Style.DIM
            if br in self.workbranch.get_work_branch_history():
                color = Fore.WHITE
            if br == wrk:
                color = Fore.CYAN
            if current_br == branch:
                color = Fore.GREEN
            if branch not in current_local_branches:
                color = Fore.LIGHTRED_EX + Style.DIM
            print(color + str(i) + " " + str(branch) + Style.RESET_ALL)

    def checkout_from_history(self, idx):
        history = self.checkoutHistory.get_checkout_history()
        history.reverse()
        if not self.full:
            history = dedup(history)

        branch = history[idx]

        if self.git.is_existing_branch(branch):
            self.checkout(branch)
        else:
            print("The branch does not exist any more")

    def checkout_main(self):
        main = str(self.cleanup.get_main_branch())
        if main == 'None':
            print("You have to set a main branch first!")
        else:
            self.checkout(main)

    def checkout_work(self):
        wrk = str(self.workbranch.get_work_branch())
        if wrk == 'None':
            print("You have to set a work branch first!")
        else:
            self.checkout(wrk)

