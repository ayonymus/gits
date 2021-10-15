from cli.tools import confirm
from cli.tools import YES
from cli.tools import CANCEL

from features.cleanup import Cleanup


class CleanupCli:

    def __init__(self, git, branch_cleanup):
        self.git = git
        self.branch_cleanup = branch_cleanup

    def add_subparser(self, subparsers):
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
            self.cleanup(args.branch, False)
        elif args.branch is None:
            print("Define a branch to clean up")

    def cleanup(self, branch, iterate):
        confirmation = confirm("This will delete '%s' branch and notes marked as 'done'. Are you sure?" % branch, iterate)
        if confirmation != YES:
            return confirmation
            
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
            print("Branch is not merged!", self.git.branch())

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
        for branch in self.git.branches():
            validate = self.branch_cleanup.validate_branch(branch.name)
            if validate == Cleanup.CURRENT_BRANCH:
                print("Skipping current branch... \n") 
            else:
                result = self.cleanup(branch, True)
                if result == CANCEL:
                    print('Cleanup cancelled')
                    break
