from tabulate import tabulate
from termcolor import colored

from cli.color import apply_color, Current, Main, Work, Important
from features.tags.tags import TagsHandler
from tools.githelper import GitHelper


RIGHT = "\u25b6"
UP = "\u25b2"
LEFT = "\u25c0"
DOWN = "\u25bc"

UPSTREAM = UP
PUSHED = colored(UP, 'green')
MERGED = LEFT
NO_UPSTREAM = colored(UP, 'red')


class OverviewCli:

    def __init__(self, git: GitHelper, tags_handler: TagsHandler):
        self.git = git
        self.tags_handler = tags_handler

    def overview(self, fetch):
        if fetch:
            print("Fetch...")
            self.git.fetch()

        tags = self.tags_handler.get_tags()
        main = tags.main
        cur = str(self.git.current_branch())

        data = []
        for i, branch in enumerate(self.git.branches_str()):
            upstream = self.upstream_status(branch, main)
            branch_colored = apply_color(branch, tags, False, cur)
            data.append([branch_colored, upstream])

        print(tabulate(data, headers=["Branch", "State"]))
        print()
        self.print_legend()

    def print_legend(self):
        print(f"{Current} {Main} {Work} {Important} Regular")
        print(
            f"{PUSHED} Sync w/ origin",
            f"{UPSTREAM} Has remote",
            f"{NO_UPSTREAM} No remote, not on {Main}",
            f"{MERGED} Merged to {Main}")

    def upstream_status(self, branch, main):
        is_pushed = self.git.is_pushed(branch)
        has_upstream = self.git.has_remote(branch)
        is_merged = self.git.is_merged(branch, main)

        if is_pushed:
            state = PUSHED
        elif has_upstream:
            state = UPSTREAM
        elif is_merged:
            state = LEFT
        else:
            state = NO_UPSTREAM
        return state
