#!/usr/bin/env python3

import argparse
import sys

from data.store import Storage2
from features.checkout2.checkout import CheckoutHandler, CheckoutStore
from features.checkout2.checkout_cli import CheckoutCli
from features.cleanup.cleanup_cli import CleanupCli
from features.cleanup.cleanup_handler import CleanupHandler
from features.notes.notes_cli import NotesCli
from features.notes.notes_handler import NotesHandler, NotesStore
from features.overview_cli import OverviewCli
from features.review.review_cli import ReviewCli
from features.review.review_handler import ReviewHandler
from features.tags.tags import TagsStorage, TagsHandler
from features.tags.tags_cli import TagsCli
from features.work.work import WorkHandler
from features.work.work_cli import WorkCli
from tools.githelper import GitHelper


class Gits:
    """
    CLI entry point to the program.

    Should not contain any logic apart from mapping arguments to methods
    and printing results to command line.
    """

    def __init__(self):
        git = GitHelper()

        storage2 = Storage2(git.work_dir())

        tags_handler = TagsHandler(TagsStorage(storage2), git)
        self.tags_cli = TagsCli(tags_handler)
        self.overview = OverviewCli(git, tags_handler)

        checkout_handler = CheckoutHandler(CheckoutStore(storage2), git, tags_handler)
        self.checkout_cli = CheckoutCli(checkout_handler, self.overview)

        work_handler = WorkHandler(tags_handler, checkout_handler, git)
        self.work_cli = WorkCli(work_handler)

        cleanup_handler = CleanupHandler(git, tags_handler)
        self.cleanup_cli = CleanupCli(cleanup_handler)

        notes_handler = NotesHandler(store=NotesStore(storage2), git=git)
        self.notes_cli = NotesCli(notes_handler)

        self.review_cli = ReviewCli(ReviewHandler(git=git, tags=tags_handler))

    def main(self):
        parser = argparse.ArgumentParser(description='Keep track of work when working on multiple branches')
        parser.add_argument("-o", "--overview", action="store_true", help="List local branches with additional data")
        parser.add_argument("-f", "--fetch", action="store_true", help="Do a fetch before overview")

        subparsers = parser.add_subparsers()

        self.checkout_cli.add_subparser(subparsers)
        self.work_cli.add_subparser(subparsers)
        self.notes_cli.add_subparser(subparsers)
        self.tags_cli.add_subparser(subparsers)
        self.cleanup_cli.add_subparser(subparsers)
        self.review_cli.add_subparser(subparsers)
        args = parser.parse_args()

        if not len(sys.argv) > 1:
            parser.print_help()
            exit(0)
        self.__handle_args__(args)

    def __handle_args__(self, args):
        if args.overview:
            self.overview.overview(False)
            pass
        elif args.fetch:
            self.overview.overview(True)
            pass
        else:
            args.func(args)


if __name__ == '__main__':
    Gits().main()

