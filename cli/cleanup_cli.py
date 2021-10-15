from cli.tools import confirm
from cli.tools import CANCEL

from features.cleanup import Cleanup

OK = 0
SKIP = 1
BREAK = 2
DONE = 10

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
        cleanup_parser.add_argument("-m", "--main", action="store_true", help="Print main branch")
        cleanup_parser.add_argument("--setmain", action="store_true", help="Set the main branch")
        
        
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
        elif args.main:
            print("Main branch is %s" % self.branch_cleanup.get_main_branch())
        elif args.setmain:
            self.set_main_branch()
        elif args.branch is None:
            print("Please define a branch to clean up")

    def cleanup(self, branch, iterate):
        validatation = self.__validate_branch__(branch) 
        if validatation != OK: return validatation
        
        confirmation = confirm("This will delete '%s' branch and notes marked as 'done'. Are you sure?" % branch, iterate)
        if confirmation == CANCEL:
            print('Cleanup cancelled')
            return BREAK
            
        result = self.branch_cleanup.cleanup(branch)
        if Cleanup.SUCCESS == result:
            print("Branch and tasks deleted")
            return DONE
        if Cleanup.ERROR == result:
            print("Something went wrong, branch could not be deleted")
        if Cleanup.NOT_EXIST == result:
            print("Branch does not exist")
        if Cleanup.NOT_MERGED == result:
            print("Branch is not merged!", self.git.branch())

    def __validate_branch__(self, branch):
        validate = self.branch_cleanup.validate_branch(branch.name)
        if validate == Cleanup.MAIN_BRANCH_NOT_SET:
            print("You must set up a main branch before doing a cleanup.")
            self.set_main_branch()            
            return BREAK
        elif validate == Cleanup.NOT_MAIN_BRANCH:
            print("Cleanup should be started from the main branch! (%s)" % self.branch_cleanup.get_main_branch())
            return BREAK
        elif validate == Cleanup.CURRENT_BRANCH:
            print("Skipping currently checked out branch ('%s')" % branch)
            return SKIP
        elif validate == Cleanup.BRANCH_IGNORED:
            print("Skipping branch on ignore list ('%s')" % branch)
            return SKIP
        elif validate == Cleanup.HAS_OPEN_TASKS:
            print("Skippin branch: there are still open tasks. ('%s')" % branch)
            return SKIP
        else: 
            return OK

    def set_main_branch(self):
        ans = input("Please enter main branch name: ").lower()
        result = self.branch_cleanup.add_main_branch(ans)
        if (result):
            print("Main branch is now: %s" % ans )
        else:
            print("No such branch in repository!")
            exit(1)


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
        cleaned = []
        skipped = []
        for branch in self.git.branches():
            result = self.cleanup(branch, True)
            if result is BREAK:
                break
            elif result is SKIP:
                skipped.append(branch.name)
            elif result is DONE:
                cleaned.append(branch.name)
        print("\n")   
        if len(cleaned) > 0 or len(skipped) > 0:
            print("Summary")
            print("Removed: ", cleaned)
            print("Skipped: ", skipped)

        
