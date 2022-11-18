from cli.color import deleted, Main, work, Important, important, Work, error, warn
from cli.tools import YES, NO, CANCEL, confirm
from features.cleanup.cleanup_handler import CleanupHandler, Validation


OK = 0
SKIP = 1
BREAK = 2
NOT_MERGED = 3
DONE = 10


class CleanupCli:

    def __init__(self, handler: CleanupHandler):
        self.handler = handler

    def add_subparser(self, subparsers):

        parser = subparsers.add_parser('cleanup', help=f'Perform checks before a branch is {deleted("deleted")}')
        parser.add_argument("branch", nargs="?", default=None,
                            help=f'Perform checks and {deleted("deletes")} branch. '
                                 f'Required to set up a {Main} branch in order to detect unmerged changes')
        parser.add_argument("--iterate", action="store_true",
                            help=f'{deleted("Delete")} branches iteratively')
        parser.add_argument("-D", action="store_true",
                            help=f'Prompt for {deleted("deleting")} unmerged branches anyways')
        parser.set_defaults(func=self.handle)

    def handle(self, args):
        if args.iterate:
            self.iterative_cleanup(args.D)
        elif args.branch is not None:
            print("abrbr ", args.branch)
            self.validate_and_cleanup(args.branch, False, args.D)

    def validate_and_cleanup(self, branch, iterate, hard):
        validation = self.validate(branch, hard)
        if validation is not OK and validation is not NOT_MERGED:
            return SKIP
        else:
            print()
            return self.cleanup(branch, iterate, (hard and validation == NOT_MERGED))

    def cleanup(self, branch, iterate, delete_unmerged):
        print(f'You are about to delete \'{warn(branch)} \' branch.')
        confirmation = confirm("Are you sure?", iterate)
        if confirmation == CANCEL:
            print(warn("Cleanup cancelled"))
            return BREAK
        if confirmation == NO:
            print(warn("Skipping branch"))
            return SKIP

        if delete_unmerged:
            print(f'The branch contains changes not merged to the {Main} branch.')
            confirmation = confirm(f'{error("Caution: Deleting this branch may lead to data loss!")} Delete anyways?', False)
            if confirmation == NO:
                print(warn("Skipping branch"))
                return SKIP

        result = self.handler.delete(branch, delete_unmerged)
        if result:
            print("Branch deleted")
            return DONE
        else:
            print("Error deleting branch")
            return SKIP

    def iterative_cleanup(self, hard):
        cleaned = []
        skipped = []
        for branch in self.handler.get_branches():
            result = self.validate_and_cleanup(branch, True, hard)
            if result is BREAK:
                break
            elif result is SKIP:
                skipped.append(branch)
            elif result is DONE:
                cleaned.append(branch)
        print("")
        if len(cleaned) > 0 or len(skipped) > 0:
            print("Summary")
            print("Removed: ", cleaned)
            print("Skipped: ", skipped)
        pass

    def validate(self, branch, hard_enabled):
        result = self.handler.validate_branch(branch)
        match result:
            case Validation.NOT_EXIST:
                print("Branch does not exist!")
                return BREAK
            case Validation.MAIN_NOT_SET:
                print("You must set up a main branch before doing a cleanup.")
                return BREAK
            case Validation.CURRENT:
                print("Skipping currently checked out branch ('%s')" % branch)
                return SKIP
            case Validation.MAIN:
                print(f"Skipping {Main} branch: {work(branch)}")
                return SKIP
            case Validation.WORK:
                print(f"Skipping {Work} branch: {work(branch)}")
                return SKIP
            case Validation.IMPORTANT:
                print(f"Skipping {Important} branch: {important(branch)}")
                return SKIP
            case Validation.NOT_MERGED_TO_MAIN:
                if hard_enabled:
                    return NOT_MERGED
                else:
                    print(f"Skipping branch: {branch} - not merged to {Main}. Use -D option to delete anyways")
                    return SKIP
            case Validation.OK_TO_DELETE:
                return OK
        print(f'Skipping branch: {error("Validation error.")}')
        return SKIP
