from tabulate import tabulate

from cli.tools import is_nix
from features.review.review_handler import ReviewHandler


class ReviewCli:

    def __init__(self, review_handler: ReviewHandler):
        self.review_handler=review_handler

    def add_subparser(self, subparser):
        parser = subparser.add_parser("review", help="Quickly have a look at a team mate's work")
        parser.add_argument("-r", "--remotes", nargs='?', const=10, type=int,
                            help="Show most recently updated remote branches")
        if is_nix():
            parser.add_argument("-s", "--select", action="store_true",
                                help=f'Select branch to review from list')
        parser.set_defaults(func=self.handle_review)

    def handle_review(self, args):
        if args.remotes:
            self.__print_remotes__(args.remotes)

    def __print_remotes__(self, remotes):
        branches = self.review_handler.get_remotes()[:remotes]
        data = []
        for i, branch in enumerate(branches):
            data.append([i, branch])
        print(tabulate(data, headers=["Nr", "Branch"]))
