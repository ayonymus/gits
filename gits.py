#!/usr/bin/env python3

import argparse
import sys

from tools.checkout import CheckoutHistory
from tools.cleanup import Cleanup
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
        self.checkoutHistory = CheckoutHistory(self.git, storage)
        self.workbranch = Workbranch(self.git, storage,self.checkoutHistory)
        self.branch_cleanup = Cleanup(self.git, storage, self.workbranch, self.tasks)

    def print_current_work_branch(self):
        current = self.workbranch.get_work_branch()
        print("Current work branch is", ("not set" if current is None else current))

    def print_work_branch_history(self):
        for i, branch in enumerate(self.workbranch.get_work_branch_history()):
            print(i, branch)

    def set_work_branch(self):
        branch = self.workbranch.set_work_branch()
        print("Current work branch is %s" % branch)

    def checkout_work_branch(self):
        branch = self.workbranch.checkout_work_branch()
        print("Switched to branch '%s'" % branch)

    def checkout_work_branch_history(self, index):
        branch = self.workbranch.checkout_work_branch_from_history(index)
        print("No such branch" if branch is None else "Switched to branch '%s'" % branch)

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

    def checkout(self, branch, new_branch=False):
        result = self.checkoutHistory.checkout(branch, new_branch)
        if result:
            print("Current branch is \n %s" % branch)
        else:
            print("Could not check out branch")

    def checkout_history(self):
        for i, branch in enumerate(self.checkoutHistory.get_checkout_history()):
            print(i, branch)
        print()

    def cleanup(self, branch):
        if not Gits.confirm("This will delete '%s' branch and notes marked as 'done'. Are you sure?" % branch):
            return
        result = self.branch_cleanup.cleanup(branch)
        if Cleanup.SUCCESS == result:
            print("Branch and tasks deleted")
        if Cleanup.ERROR == result:
            print("Something went wrong, branch could not be deleted")
        if Cleanup.NOT_MASTER_OR_DEV == result:
            print("Script should be called from 'master' or 'development' branch")
        if Cleanup.HAS_OPEN_TASKS == result:
            print("There are still open tasks. Review")
        if Cleanup.NOT_EXIST == result:
            print("Branch does not exist")
        if Cleanup.NOT_MERGED == result:
            print("Branch is not merged to", self.git.branch())

    def cleanup_add_whitelist(self, branch):
        self.branch_cleanup.add_to_whitelist(branch)
        print("'%s' added to white list" % branch)

    def cleanup_remove_from_whitelist(self, branch):
        result = self.branch_cleanup.remove_from_whitelist(branch)
        if result:
            print("'%s' removed from white list" % branch)
        else:
            print("'%s' not found in white list" % branch)

    def cleanup_print_whitelist(self):
        whitelist = self.branch_cleanup.get_whitelist()
        print("White listed branches:")
        for branch in whitelist:
            print(branch)

    def iterative_cleanup(self):
        for head in self.git.branches():
            self.cleanup(head)

    def handle_work(self, args):
        if args.s:
            self.set_work_branch()
        elif args.c:
            self.checkout_work_branch()
        elif args.ch:
            self.checkout_work_branch_history(args.W)
        elif args.history:
            self.print_work_branch_history()
        else:
            self.print_current_work_branch()

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

    def handle_checkout(self, args):
        if args.checkout is not None:
            self.checkout(args.checkout)
        elif args.branch:
            self.checkout(args.branch, True)
        elif args.history:
            self.checkout_history()
        elif args.suffix:
            self.checkout("%1s_%2s" % (self.git.branch(), args.suffix), True)

    def handle_cleanup(self, args):
        if args.addw:
            self.cleanup_add_whitelist(args.addw)
        elif args.removew:
            self.cleanup_remove_from_whitelist(args.removew)
        elif args.whitelist:
            self.cleanup_print_whitelist()
        elif args.iterate:
            self.iterative_cleanup()
        elif args.branch is not None:
            self.cleanup(args.branch)
        elif args.branch is None:
            print("Define a branch to clean up")

    @staticmethod
    def confirm(question):
        print(question)
        ans = input('(Y/N) << ').lower()
        if ans in ['yes', 'y']:
            return True
        if ans in ['no', 'n']:
            return False

    def main(self):
        parser = argparse.ArgumentParser(description='Keep track when working with multiple branches on git')
        subparsers = parser.add_subparsers()

        work_parser = subparsers.add_parser('work', help="Keep track of a currently important branch")
        work_parser.add_argument("current", nargs="?", type=str, default=None, help="Show current work branch")
        work_parser.add_argument("-s", action="store_true", help="Set current work branch")
        work_parser.add_argument("-c", action="store_true", help="Checkout current work branch")
        work_parser.add_argument("-ch", type=int,  help="Checkout work branch from history by id")
        work_parser.add_argument("-H", "--history", action="store_true", help="Show work branch history")
        work_parser.set_defaults(func=self.handle_work)

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

        # Checkout
        checkout_parser = subparsers.add_parser('checkout', help="Keep a history of checked out branches")
        checkout_parser.add_argument("checkout", nargs="?", type=str, default=None,
                                     help="Check out branch and add to checkout history")
        checkout_parser.add_argument("-b", "--branch", type=str, default=None,
                                     help="Create new branch, check out, and add to checkout history")
        checkout_parser.add_argument("-H", "--history", action="store_true", help="Check out history")
        checkout_parser.add_argument("--suffix", type=str,
                                     help="Create and check out branch with current's name plus a suffix")
        checkout_parser.set_defaults(func=self.handle_checkout)

        # Cleanup
        cleanup_parser = subparsers.add_parser('cleanup', help="Clean up when done working with a branch")
        cleanup_parser.add_argument("branch", nargs="?", type=str, default=None,
                                    help="Check open tasks, remove done tasks for branch, delete branch. "
                                         "Run from master or development branch")
        cleanup_parser.add_argument("--addw", type=str,
                                    help="White list a branch so that it's not cleaned up")
        cleanup_parser.add_argument("--removew", type=str,
                                    help="Remove a branch from white list")
        cleanup_parser.add_argument("--iterate", action="store_true",
                                    help="Iterates over all local branches and offers to clean up if not white listed")
        cleanup_parser.add_argument("-w", "--whitelist", action="store_true", help="Print white list")
        cleanup_parser.set_defaults(func=self.handle_cleanup)

        args = parser.parse_args()

        if not len(sys.argv) > 1:
            parser.print_help()
            exit(0)

        args.func(args)


if __name__ == '__main__':
    Gits().main()
