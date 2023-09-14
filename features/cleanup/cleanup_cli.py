from cli.color import deleted, Main, work, Important, important, Work, error, warn
from cli.tools import YES, NO, CANCEL, confirm, is_nix
from features.cleanup.cleanup_handler import CleanupHandler, Validation


OK = 0
SKIP = 1
BREAK = 2
NOT_MERGED = 3
NOT_SYNCED = 4
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
        if is_nix():
            parser.add_argument("-s", "--select", action="store_true",
                            help=f'{deleted("Delete")} branch selected from list')
        parser.add_argument("-D", action="store_true",
                            help=f'Prompt for {deleted("deleting")} unmerged branches anyways')
        parser.add_argument("-r", action="store_true",
                            help=f'{deleted("Delete")} the remote branch as well')
        parser.set_defaults(func=self.handle)

    def handle(self, args):
        if args.iterate:
            self.iterative_cleanup(args.D, args.r)
        elif args.branch is not None:
            self.validate_and_cleanup(args.branch, iterate=False, delete_unmerged=args.D, delete_remote=args.r)
        elif is_nix() and args.select is not None:
            self.select(delete_unmerged=args.D, delete_remote=args.r)

    def validate_and_cleanup(self, branch, iterate, delete_unmerged, delete_remote):
        validation = self.validate(branch, delete_unmerged)
        if validation is OK:
            return self.cleanup(branch, iterate, False, False, delete_remote)
        elif validation is NOT_MERGED:
            return self.cleanup(branch, iterate, False, True, delete_remote)
        elif validation is NOT_SYNCED:
            return self.cleanup(branch, iterate, True, True, delete_remote)
        else:
            return SKIP

    def select(self, delete_unmerged, delete_remote):
        branches = self.handler.get_branches()
        from cli.selector import ListSelector
        selector = ListSelector(branches, lambda i: self.validate_and_cleanup(branches[i], False, delete_unmerged, delete_remote))
        selector.start()

    def cleanup(self, branch, iterate, not_synced, delete_unmerged, delete_remote):
        print(f'You are about to delete \'{warn(branch)}\' branch.')
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

        if not_synced:
            print(f'The branch contains changes not in sync with the remote branch.')
            confirmation = confirm(f'{error("Caution: Deleting this branch may lead to data loss!")} Delete anyways?', False)
            if confirmation == NO:
                print(warn("Skipping branch"))
                return SKIP

        result = self.handler.delete(branch, delete_unmerged)

        if not result:
            print("Error deleting branch")
            return SKIP
        else:
            print("Branch deleted")

        if self.handler.has_remote(branch) and delete_remote:
            confirmation = confirm(f'Are you sure you want to {deleted("delete")} the remote branch?', False)
            if confirmation == YES:
                result = self.handler.git.delete_remote(branch)
                if result:
                    print("Remote branch deleted")
                else:
                    print("There was an error deleting the remote branch")
            else:
                print("Remote branch not deleted")
        return DONE

    def iterative_cleanup(self, hard, remote):
        cleaned = []
        skipped = []
        for branch in self.handler.get_branches():
            result = self.validate_and_cleanup(branch, True, hard, remote)
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
            case Validation.NOT_SYNC_WITH_REMOTE:
                if hard_enabled:
                    return NOT_SYNCED
                else:
                    print(f"Skipping branch: {branch} - not in sync with remote. Use -D option to delete anyways")
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
