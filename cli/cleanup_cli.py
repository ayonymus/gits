from cli.tools import confirm
from cli.tools import CANCEL
from cli.tools import NO
from cli.tools import YES

from features.cleanup import Cleanup

from termcolor import colored

OK = 0
SKIP = 1
BREAK = 2
DONE = 10

G = "green"
R = "red"
Y = "yellow"

class CleanupCli:

    def __init__(self, git, branch_cleanup):
        self.git = git
        self.branch_cleanup = branch_cleanup

    def add_subparser(self, subparsers):
        cleanup_parser = subparsers.add_parser('cleanup', help="Clean up when done working with a branch")
        cleanup_parser.add_argument("branch", nargs="?", type=str, default=None,
                                    help="Check open tasks, remove done tasks for branch, delete branch. "
                                         "Required to run from the main branch in order to detect unmerged changes. "
                                         "Unmerged branches (relative to main) will not be deleted." )
        cleanup_parser.add_argument("--addi", type=str,
                                    help="Ignore list a branch so that it's not cleaned up")
        cleanup_parser.add_argument("--removei", type=str,
                                    help="Remove a branch from ignore list")
        cleanup_parser.add_argument("--iterate", action="store_true",
                                    help="Iterates over all local branches and offers to clean up if not ignore listed")
        cleanup_parser.add_argument("-D", action="store_true",
                                    help="Flag to prompt for unmerged branch to delete")
        cleanup_parser.add_argument("-i", "--ignorelist", action="store_true", help="Print ignored branch list")
        cleanup_parser.add_argument("-m", "--main", action="store_true", help="Print main branch")
        cleanup_parser.add_argument("--setmain", action="store_true", help="Set the main branch")
        cleanup_parser.set_defaults(func=self.handle_cleanup)

    def handle_cleanup(self, args):
        if args.addi:
            self.cleanup_add_ignorelist(args.addi)
        elif args.removei:
            self.cleanup_remove_from_ignorelist(args.removei)
        elif args.ignorelist:
            self.cleanup_print_ignorelist()
        elif args.iterate:
            self.iterative_cleanup(args.D)
        elif args.branch is not None:
            self.cleanup(args.branch, False, args.D)
        elif args.main:
            print("Main branch is %s" % self.branch_cleanup.get_main_branch())
        elif args.setmain:
            self.set_main_branch()
        elif args.branch is None:
            print("Please define a branch to clean up")

    def cleanup(self, branch, iterate, hard_enabled):
        validatation = self.__validate_branch__(branch, hard_enabled) 
        if validatation != OK: return validatation
        
        print("\nYou are about to delete '", colored(branch, Y), "' branch and remove associated tasks.")
        confirmation = confirm("Are you sure?", iterate)
        if confirmation == CANCEL:
            print(colored('Cleanup cancelled', Y))
            return BREAK
        if confirmation == NO:
            print(colored('Skipping branch', Y))
            return SKIP

        result = self.branch_cleanup.cleanup(branch)
        if Cleanup.SUCCESS == result:
            print(colored("Branch and tasks deleted", G))
            return DONE
        if Cleanup.ERROR == result:
            print(colored("Something went wrong, branch could not be deleted", R))
        if Cleanup.NOT_EXIST == result:
            print(colored("Branch does not exist!", R))
        if Cleanup.NOT_MERGED == result:
            print(colored("Commits not merged to main.", Y))
            if hard_enabled:
                confirmation = confirm(colored("Caution: Deleting this branch may lead to data loss!", R) + " Delete anyways? ", False)
                if (confirmation == YES):
                    retry = self.branch_cleanup.cleanup(branch, True)
                    if Cleanup.SUCCESS == retry:
                        print(colored("Branch and tasks deleted", G))
                        return DONE              
            print(colored('Skipping branch', Y))
        return SKIP

    def __validate_branch__(self, branch, hard_enabled):
        validate = self.branch_cleanup.validate_branch(branch)
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
            print("Skipping branch: there are still open tasks. ('%s')" % branch)
            return SKIP
        elif validate == Cleanup.NOT_MERGED:
            if hard_enabled:
                return OK
            else:
                print("Skipping branch: not merged to main (%s). Use -D option to delete anyways" % branch)
                return SKIP  
        elif validate == Cleanup.OK_TO_DELETE:
            return OK
        else:
            print("Validation went wrong. ('%s')" % branch)
            return SKIP

    def set_main_branch(self):
        ans = input("Please enter main branch name: ").lower()
        result = self.branch_cleanup.add_main_branch(ans)
        if (result):
            print("Main branch is now: %s" % ans )
        else:
            print("No such branch in repository!")
            exit(1)

    def cleanup_add_ignorelist(self, branch):
        self.branch_cleanup.add_to_ignorelist(branch)
        print("'%s' added to ignore list" % branch)

    def cleanup_remove_from_ignorelist(self, branch):
        result = self.branch_cleanup.remove_from_ignorelist(branch)
        if result:
            print("'%s' removed from ignore list" % branch)
        else:
            print("'%s' was not found in ignore list" % branch)

    def cleanup_print_ignorelist(self):
        ignorelist = self.branch_cleanup.get_ignorelist()
        print("ignore listed branches:")
        for branch in ignorelist:
            print(branch)

    def iterative_cleanup(self, hard):
        cleaned = []
        skipped = []
        for branch in self.git.branches():
            result = self.cleanup(branch.name, True, hard)
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
