from features.checkout2.checkout import CheckoutHandler
from features.tags.tags_cli import Deleted, Main, Work


class CheckoutCli:

    def __init__(self, handler: CheckoutHandler):
        self.handler = handler

    def add_subparser(self, subparsers):
        parser = subparsers.add_parser('checkout',
                                       help="Keep a log of checked out branches in a more readable way than reflog")
        parser.add_argument("checkout", nargs="?", type=str, default=None,
                            help="Check out branch and add to checkout history")
        parser.add_argument("-b", "--branch", type=str,
                            help="Create new branch, check out, and add to checkout logs")
        parser.add_argument("--suffix", type=str,
                            help="Create and check out branch with current branches name plus _suffix")
        parser.add_argument("-l", "--logs", nargs='?', const=10, type=int,
                            help="Show truncated checkout logs. Provide -f flag for full list.")
        parser.add_argument("-f", "--full", action="store_true", help="Use full log list.")
        parser.add_argument("-m", "--main", action="store_true", help=f"Check out {Main} branch")
        parser.add_argument("-w", "--work", action="store_true", help=f"Check out {Work} branch")
        parser.set_defaults(func=self.handle_checkout)

    def handle_checkout(self, args):
        if args.checkout is not None:
            self.print_message(self.handler.checkout(args.checkout))
        elif args.branch:
            self.print_message(self.handler.checkout(args.branch, True))
        elif args.suffix:
            self.print_message(self.handler.checkout_suffix(args.suffix))
        elif args.main:
            self.print_message(self.handler.checkout_main())
        elif args.work:
            self.print_message(self.handler.checkout_work())
        elif args.logs:
            self.print_logs(args.logs, args.full)

    def print_message(self, branch):
        if branch is not None:
            print(f"Switched to branch '{branch}'")

    def print_logs(self, length, full):
        logs = self.handler.get_logs(length, full)
        for log in logs:
            print(f'{log[0]} {Deleted if log[2] else ""}')

