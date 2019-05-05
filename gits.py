import argparse

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
        self.workbranch = Workbranch(storage,self.checkoutHistory, self.git)
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
        print("Assigned to '%s'" % branch)

    def print_tasks(self):
        br = self.git.branch()
        print("Tasks for %s branch:" % br)
        for i, task in enumerate(self.tasks.get_tasks(br)):
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
        print("Done tasks for %s branch:" % br)
        for i, task in enumerate(self.tasks.get_done_tasks(br)):
            print(i, task)
        print()

    def checkout(self, branch):
        self.checkoutHistory.checkout(branch)

    def checkout_history(self):
        for i, branch in enumerate(self.checkoutHistory.get_checkout_history()):
            print(i, branch)
        print()

    def cleanup(self, branch):
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

    def main(self):
        parser = argparse.ArgumentParser(description='Works. Branching related everyday tasks')
        parser.add_argument("-s", help="Set current work branch", action="store_true")
        parser.add_argument("-w", help="Checkout current work branch", action="store_true")
        parser.add_argument("-W", help="Checkout work branch from history by id", type=int)
        parser.add_argument("-H", "--history", help="Show work branch history", action="store_true")
        parser.add_argument("-t", help="Assign a task to current work branch", type=str)
        parser.add_argument("--tasks", help="List tasks assigned to current work branch", action="store_true")
        parser.add_argument("-r", help="Remove task by id", type=int)
        parser.add_argument("--done", nargs=1, help="Set task done by id", type=int)
        parser.add_argument("--listdone", help="Set task done by id", action="store_true")
        parser.add_argument("-m", nargs=2, help="Move task in list", type=int)
        parser.add_argument("--movetop", help="Move task to top in list", type=int)
        parser.add_argument("--task", nargs=2, help="Assign a task to arbitrary branch. [0] branch name, [1] task", type=str)
        parser.add_argument("-c", help="Check out branch and add to history", type=str)
        parser.add_argument("-ch", help="Check out history", action="store_true")
        parser.add_argument("--cleanup", help="Cleanup", type=str)

        # task should have a date
        # work branch could have a date
        # switch - commit everything to branch, commit title _WORK_IN_PROGRESS_ --

        args = parser.parse_args()
        if args.history:
            self.print_work_branch_history()
            return
        if args.s:
            self.set_work_branch()
            return
        if args.w:
            self.checkout_work_branch()
            return
        if args.W:
            self.checkout_work_branch_history(args.W)
            return
        if args.t:
            self.assign_task(args.t)
            return
        if args.tasks:
            self.print_tasks()
            return
        if args.done:
            self.set_task_done(args.done[0])
            return
        if args.r:
            self.remove_task(args.r)
            return
        if args.m:
            self.move_task(args.m[0], args.m[1])
            return
        if args.movetop:
            self.move_task(args.movetop, 0)
            return
        if args.task:
            self.assign_to_branch(args.task[0], args.task[1])
            return
        if args.listdone:
            self.print_done()
            return
        if args.c:
            self.checkout(args.c)
            return
        if args.ch:
            self.checkout_history()
            return
        if args.cleanup:
            self.cleanup(args.cleanup)
            return
        self.print_current_work_branch()


if __name__ == '__main__':
    Gits().main()
