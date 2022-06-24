
from colorama import Fore, Style

class CheckoutCli:

    def __init__(self, git, checkout_history, workbranch, cleanup):
        self.git = git
        self.checkoutHistory = checkout_history
        self.workbranch = workbranch
        self.cleanup = cleanup
        self.full = False

    def add_subparser(self, subparsers):
        checkout_parser = subparsers.add_parser('checkout', help="Keep a history of checked out branches")
        checkout_parser.add_argument("checkout", nargs="?", type=str, default=None,
                                     help="Check out branch and add to checkout history")
        checkout_parser.add_argument("-b", "--branch", type=str, default=None,
                                     help="Create new branch, check out, and add to checkout history")
        checkout_parser.add_argument("--suffix", type=str,
                                     help="Create and check out branch with current's name plus a suffix")
        checkout_parser.add_argument("-H", "--history", action="store_true", help="Check out history, duplicates removed, most recent first")
        checkout_parser.add_argument("-bh", "--branchhistory", type=int,
                                     help="Check out a branch from branch history based by id")
        checkout_parser.add_argument("-f", "--full", action="store_true", help="Check out full history. Combine with -H and -bh")
        checkout_parser.add_argument("-l", "--last", type=int, help="Check out x from last branch from history")
        checkout_parser.add_argument("-m", "--main", action="store_true", help="Check main branch")
        checkout_parser.add_argument("-w", "--work", action="store_true", help="Check work branch")

        checkout_parser.set_defaults(func=self.handle_checkout)

    def handle_checkout(self, args):
        if args.full:
            self.full = True
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
            self.checkout_last(args.last)
        elif args.main:
            self.checkout_main()
        elif args.work:
            self.checkout_work()

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
        history = self.checkoutHistory.get_checkout_history()
        history.reverse()
        if not self.full:
            history = self.dedup(history)
        current_br = str(self.git.branch())

        for i, branch in enumerate(history):
            br = str(branch)
            color = Style.DIM
            if br in self.workbranch.get_work_branch_history():
                color = Fore.WHITE
            if br == wrk:
                color = Fore.CYAN
            if current_br == branch:
                color = Fore.GREEN
            print(color + str(i) + " " + str(branch) + Style.RESET_ALL)

    def dedup(self, my_list):
        seen = {}
        new_list = [seen.setdefault(x, x) for x in my_list if x not in seen]
        return new_list

    def checkout_from_history(self, id):
        history = self.checkoutHistory.get_checkout_history()
        history.reverse()
        if not self.full:
            history = self.dedup(history)

        branch = history[id]

        if self.git.is_existing_branch(branch):
            self.checkout(branch)
        else:
            print("The branch does not exist any more")

    def checkout_last(self, x):
        branch_list = self.checkoutHistory.get_checkout_history()
        branch = branch_list[len(branch_list) - 1 - x]
        self.checkout(branch)

    def checkout_main(self):
        main = str(self.cleanup.get_main_branch())
        self.checkout(main)

    def checkout_work(self):
        wrk = str(self.workbranch.get_work_branch())
        self.checkout(wrk)

