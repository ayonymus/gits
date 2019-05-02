import argparse

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
        self.workbranch = Workbranch(storage, self.git)
        self.tasks = TaskHandler(storage)

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

    def close_work(self):
        # TODO
        # Cleans up for a selected work branch.
        # 1 check left over tasks
        # 2 remove from branch list
        # 3 add to closed list
        # 4 delete local branch
        # 5 check if local and remove branch differ2
        pass

    def main(self):
        parser = argparse.ArgumentParser(description='Works. Branching related everyday tasks')
        parser.add_argument("-s", help="Set current work branch", action="store_true")
        parser.add_argument("-w", help="Checkout current work branch", action="store_true")
        parser.add_argument("-W", help="Checkout work branch from history by id", type=int)
        parser.add_argument("-H", "--history", help="Show work branch history", action="store_true")
        parser.add_argument("-t", help="Assign a task to current work branch", type=str)
        parser.add_argument("--tasks", help="List tasks assigned to current work branch", action="store_true")
        parser.add_argument("-r", help="Remove task by id", type=int)
        parser.add_argument("-d", help="Set task done by id", type=int)
        # task should have a date
        # should delete task
        # should complete task
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
        if args.d:
            self.set_task_done(args.d)
            return
        if args.r:
            self.remove_task(args.r)
            return
        self.print_current_work_branch()


if __name__ == '__main__':
    Gits().main()