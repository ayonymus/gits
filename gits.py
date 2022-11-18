#!/usr/bin/env python3

import argparse
import sys

import colorama

from cli.tasks_cli import TasksCli
from features.checkout2.checkout import CheckoutHandler, CheckoutStore
from features.overview_cli import OverviewCli
from data.store import Storage2
from features.tags.tags import TagsStorage, TagsHandler
from features.tags.tags_cli import TagsCli
from features.taskhandler import TaskHandler
from features.work.work import WorkHandler
from tools.githelper import GitHelper
from tools.storage import Storage

colorama.init()


class Gits:
    """
    CLI entry point to the program.

    Should not contain any logic apart from mapping arguments to methods
    and printing results to command line.
    """

    def __init__(self):
        git = GitHelper()
        storage = Storage(git.work_dir())

        tasks = TaskHandler(storage)

        self.tasks_cli = TasksCli(git, tasks)

        storage2 = Storage2(git.work_dir())
        tags = TagsStorage(storage2)
        tags_handler = TagsHandler(tags, git)
        self.tags_cli = TagsCli(tags_handler)

        checkout_store = CheckoutStore(storage2)
        checkout_handler = CheckoutHandler(checkout_store, git, tags_handler)
        from features.checkout2.checkout_cli import CheckoutCli
        self.checkout_cli = CheckoutCli(checkout_handler)

        work_handler = WorkHandler(tags_handler, checkout_handler, git)
        from features.work.work_cli import WorkCli
        self.work_cli = WorkCli(work_handler)

        self.overview = OverviewCli(git, tags_handler)

    def main(self):
        parser = argparse.ArgumentParser(description='Keep track when working with multiple branches on git')
        parser.add_argument("-o", "--overview", action="store_true", help="List local branches with additional data")
        parser.add_argument("-f", "--fetch", action="store_true", help="Do a fetch before overview")

        subparsers = parser.add_subparsers()

        self.checkout_cli.add_subparser(subparsers)
        self.work_cli.add_subparser(subparsers)

        self.tasks_cli.add_subparser(subparsers)
        self.tags_cli.add_subparser(subparsers)
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

