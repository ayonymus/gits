
class TasksCli:

    def __init__(self, git, tasks):
        self.git = git
        self.tasks = tasks

    def add_subparser(self, subparsers):
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
