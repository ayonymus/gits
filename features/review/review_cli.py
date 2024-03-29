import textwrap

from tabulate import tabulate

from cli.tools import is_nix, confirm, YES
from features.review.devops import DevOpsHandler
from features.review.review_handler import ReviewHandler


class ReviewCli:

    def __init__(self, review_handler: ReviewHandler):
        self.parser = None
        self.review_handler = review_handler

    def add_subparser(self, subparser):
        parser = subparser.add_parser("review", help="Quickly have a look at a team mate's work")
        self.parser = parser
        parser.add_argument("-r", "--remotes", nargs='?', const=10, type=int,
                            help="Show most recently updated remote branches")
        parser.add_argument("-p", "--pullrequests", action="store_true",
                            help="Show pull requests. Either Azure or Github must be configured")
        parser.add_argument("--configure", nargs="+", type=str,
                            help="Configure devops server: [azure {PAT} | github {PAT}] WARNING: feature is under "
                                 "development and the Personal Access Token is not stored securely!")
        if is_nix():
            parser.add_argument("-s", "--select", action="store_true",
                                help=f'Select branch to review from list')
        parser.set_defaults(func=self.handle_review)

    def handle_review(self, args):
        if args.remotes:
            self.__print_remotes__(args.remotes)
        elif args.pullrequests:
            self.__print_prs__()
        elif args.configure:
            self.__config_devops__(args.configure)
        else:
            self.parser.print_help()

    def __print_remotes__(self, remotes):
        branches = self.review_handler.get_remotes()[:remotes]
        data = []
        for i, branch in enumerate(branches):
            data.append([i, branch])
        print(tabulate(data, headers=["Idx", "Branch", "Status"]))

    def __print_prs__(self):
        prs = self.review_handler.get_prs()
        data = [(idx, pr[1], textwrap.shorten(pr[0], 25), pr[5]) for idx, pr in enumerate(prs)]
        print(tabulate(data, headers=["Idx", "Branch", "Title", "Weburl"]))

    def __config_devops__(self, configure):
        result = confirm("Warning: currently the feature is incomplete and the token is not stored securely. Continue?")
        if result == YES:
            self.review_handler.devops.configure(configure[0], configure[1])
        else:
            print("Devops access not configured.")
