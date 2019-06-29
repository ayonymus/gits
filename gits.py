#!/usr/bin/env python3

import argparse
import sys

from cli.checkout_cli import CheckoutCli
from cli.cleanup_cli import CleanupCli
from cli.work_cli import WorkCli
from features.checkout import CheckoutHistory
from features.cleanup import Cleanup
from tools.githelper import GitHelper
from tools.storage import Storage
from tools.taskhandler import TaskHandler
from tools.workbranch import Workbranch


class Gits:
    """
    CLI entry point to the program.

    Should not contain any logic apart from mapping arguments to methods
    and printing results to command line.
    """

    def __init__(self):
        self.git = GitHelper()
        storage = Storage(self.git.work_dir())
        self.tasks = TaskHandler(storage)
        checkout_history = CheckoutHistory(self.git, storage)
        self.checkout_cli = CheckoutCli(self.git, checkout_history)

        self.workbranch_cli = WorkCli(Workbranch(self.git, storage, checkout_history))

        branch_cleanup = Cleanup(self.git, storage, self.workbranch_cli, self.tasks)
        self.cleanup = CleanupCli(self.git, branch_cleanup)

    def assign_task(self, task):
        branch = self.git.branch()
        self.assign_to_branch(branch, task)

    def assign_to_branch(self, branch, task):
        self.tasks.assign_task(branch, task)
        print("Task assigned to '%s'" % branch)

    def print_tasks(self):
        br = self.git.branch()
        print("Tasks for %s branch:" % br)
        for i, task in enumerate(self.tasks.get_tasks(br)):
            print(i, task)
        print()

    def print_all_tasks(self):
        all_tasks = self.tasks.get_all_tasks()
        for branch in all_tasks.keys():
            print("Tasks for %s branch:" % branch)
            for i, task in enumerate(all_tasks[branch]):
                print(i, task)
            print()

    def remove_task(self, index):
        print("Done" if self.tasks.remove_task(self.git.branch(), index) else "No such task")

    def set_task_done(self, index):
        print("Done" if self.tasks.set_task_done(self.git.branch(), index) else "No such task")

    def move_task(self, old_pos, new_pos):
        print("Done" if self.tasks.move_task(self.git.branch(), old_pos, new_pos) else "Index error")

    def print_done(self):
        br = self.git.branch()
        print("Done tasks for '%s' branch:" % br)
        for i, task in enumerate(self.tasks.get_done_tasks(br)):
            print(i, task)
        print()

    def handle_task(self, args):
        if args.add is not None:
            self.assign_task(args.add)
        elif args.list:
            self.print_tasks()
        elif args.all:
            self.print_all_tasks()
        elif args.done:
            self.set_task_done(args.done[0])
        elif args.remove:
            self.remove_task(args.remove)
        elif args.m:
            self.move_task(args.m[0], args.m[1])
        elif args.movetop:
            self.move_task(args.movetop, 0)
        elif args.assign:
            self.assign_to_branch(args.assign[0], args.assign[1])
        elif args.donelist:
            self.print_done()
        else:
            print("Provide more arguments or check help. Until that, here are all tasks:\n")
            self.print_tasks()

    def main(self):
        parser = argparse.ArgumentParser(description='Keep track when working with multiple branches on git')
        subparsers = parser.add_subparsers()

        task_parser = subparsers.add_parser('task', help="Remember tasks for a given branch")
        task_parser.add_argument("add", nargs="?", type=str, default=None, help="Assign a task to current work branch")
        task_parser.add_argument("-l", "--list", action="store_true", help="List tasks assigned to current work branch")
        task_parser.add_argument("--all", action="store_true", help="Print all open tasks")
        task_parser.add_argument("-d", "--done", nargs=1, type=int, help="Set task done by id")
        task_parser.add_argument("--donelist", action="store_true", help="Set task done by id")
        task_parser.add_argument("-r", "--remove", type=int, help="Remove task by id")
        task_parser.add_argument("-m", nargs=2, type=int, help="Move task in list")
        task_parser.add_argument("--movetop", type=int, help="Move task to top in list")
        task_parser.add_argument("--assign", nargs=2, type=str,
                                 help="Assign a task to arbitrary branch. [0] branch name, [1] task")
        task_parser.set_defaults(func=self.handle_task)

        self.workbranch_cli.add_subparser(subparsers)
        self.cleanup.add_subparser(subparsers)
        self.checkout_cli.add_subparser(subparsers)

        args = parser.parse_args()

        if not len(sys.argv) > 1:
            parser.print_help()
            exit(0)

        args.func(args)


if __name__ == '__main__':
    Gits().main()
