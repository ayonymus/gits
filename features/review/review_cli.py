from tabulate import tabulate

from cli.color import Review
from cli.tools import is_nix
from features.review.review_handler import ReviewHandler


class ReviewCli:

    def __init__(self, review_handler: ReviewHandler):
        self.review_handler=review_handler

    def add_subparser(self, subparser):
        parser = subparser.add_parser("review", help="Quickly have a look at a team mate's work")
        parser.add_argument("checkout", nargs="?", type=str, default=None,
                            help=f"Check out remote branch, mark and add to {Review} history")
        parser.add_argument("-r", "--remotes", nargs='?', const=10, type=int,
                            help="Show most recently updated remote branches")
        if is_nix():
            parser.add_argument("-s", "--select", action="store_true",
                                help=f'Select branch to review from list')
        parser.set_defaults(func=self.__handle_review__)

    def __handle_review__(self, args):
        if args.checkout is not None:
            self.__checkout_remote__(args.checkout)
        if args.remotes:
            self.__print_remotes__(args.remotes)
        else:
            print("No argument provided")

    def __print_remotes__(self, remotes):
        branches = self.review_handler.get_remotes()[:remotes]
        data = []
        for i, branch in enumerate(branches):
            data.append([i, branch])
        print(tabulate(data, headers=["Nr", "Branch"]))

    def __checkout_remote__(self, checkout):
        pass
