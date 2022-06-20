
from colorama import Fore, Style

class CheckoutCli:

    def __init__(self, git, checkout_history, workbranch):
        self.git = git
        self.checkoutHistory = checkout_history
        self.workbranch = workbranch

    def add_subparser(self, subparsers):
        checkout_parser = subparsers.add_parser('checkout', help="Keep a history of checked out branches")
        checkout_parser.add_argument("checkout", nargs="?", type=str, default=None,
                                     help="Check out branch and add to checkout history")
        checkout_parser.add_argument("-b", "--branch", type=str, default=None,
                                     help="Create new branch, check out, and add to checkout history")
        checkout_parser.add_argument("--suffix", type=str,
                                     help="Create and check out branch with current's name plus a suffix")
        checkout_parser.add_argument("-H", "--history", action="store_true", help="Check out history")
        checkout_parser.add_argument("-bh", "--branchhistory", type=int,
                                     help="Check out a branch from branch history based by id")
        checkout_parser.add_argument("-l", "--last", action="store_true", help="Check out last branch from branch history")

        checkout_parser.set_defaults(func=self.handle_checkout)

    def handle_checkout(self, args):
        if args.checkout is not None:
            self.checkout(args.checkout)
        elif args.branch:
            self.checkout(args.branch, True)
        elif args.suffix:
            self.checkout("%1s_%2s" % (self.git.branch(), args.suffix), True)
        elif args.history:
            self.checkout_history()
        elif args.branchhistory:
            self.checkout_from_history(args.branchhistory)
        elif args.last:
            self.checkout_last()


    def checkout(self, branch, new_branch=False):
        if branch == '.':
            self.git.checkout('.')
            return
        result = self.checkoutHistory.checkout(branch, new_branch)
        if result:
            print("Current branch is \n %s" % branch)
        else:
            print("Could not check out branch")

    def checkout_history(self):
        wrk = str(self.workbranch.get_work_branch())
        wrk_hist = self.checkoutHistory.get_checkout_history()
        br = str(self.git.branch())
        for i, branch in enumerate(wrk_hist):
            color = Style.DIM
            if str(branch) in self.workbranch.get_work_branch_history():
                color = Fore.WHITE
            if str(branch) == wrk:
                color = Fore.CYAN
            if str(branch) == br:
                color = Fore.GREEN
            print(color + str(i) + " " + str(branch) + Style.RESET_ALL)

    def checkout_from_history(self, id):
        branch = self.checkoutHistory.get_checkout_history()[id]

        if self.git.is_existing_branch(branch):
            self.checkout(branch)
        else:
            print("The branch does not exist any more")

    def checkout_last(self):
        branch_list = self.checkoutHistory.get_checkout_history()
        branch = branch_list[len(branch_list) - 1]
        self.checkout(branch)