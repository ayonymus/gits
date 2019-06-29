#!/usr/bin/env python3

import argparse
import sys

from cli.checkout_cli import CheckoutCli
from cli.cleanup_cli import CleanupCli
from cli.tasks_cli import TasksCli
from cli.work_cli import WorkCli
from features.checkout import CheckoutHistory
from features.cleanup import Cleanup
from features.taskhandler import TaskHandler
from features.workbranch import Workbranch
from tools.githelper import GitHelper
from tools.storage import Storage


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
        checkout_history = CheckoutHistory(git, storage)
        workbranch = Workbranch(git, storage, checkout_history)
        branch_cleanup = Cleanup(git, storage, workbranch, tasks)

        self.tasks_cli = TasksCli(git, tasks)
        self.checkout_cli = CheckoutCli(git, checkout_history)
        self.workbranch_cli = WorkCli(workbranch)
        self.cleanup_cli = CleanupCli(git, branch_cleanup)

    def main(self):
        parser = argparse.ArgumentParser(description='Keep track when working with multiple branches on git')
        subparsers = parser.add_subparsers()

        self.tasks_cli.add_subparser(subparsers)
        self.workbranch_cli.add_subparser(subparsers)
        self.cleanup_cli.add_subparser(subparsers)
        self.checkout_cli.add_subparser(subparsers)

        args = parser.parse_args()

        if not len(sys.argv) > 1:
            parser.print_help()
            exit(0)

        args.func(args)


if __name__ == '__main__':
    Gits().main()
