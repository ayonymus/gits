from colorama import Fore, Style
from tabulate import tabulate

RIGHT = "\u25b6"
UP = "\u25b2"
LEFT = "\u25c0"
DOWN = "\u25bc"

UPSTREAM = UP
PUSHED = Fore.GREEN + UP + Fore.RESET
MERGED = LEFT
NO_UPSTREAM = Fore.RED + UP + Fore.RESET


class OverviewCli:
    """
    Functions that use separate modules
    """

    def __init__(self, git, workbranch, tasks, branch_cleanup):
        self.workbranch = workbranch
        self.git = git
        self.tasks = tasks
        self.cleanup = branch_cleanup

    def print_overview(self, fetch):
        if fetch:
            print("Fetch...")
            self.git.fetch()

        wrk = str(self.workbranch.get_work_branch())
        wrk_hist = self.workbranch.get_work_branch_history()
        cur = str(self.git.current_branch())
        cleanup_ignore = self.cleanup.get_ignorelist()
        main_br = self.cleanup.get_main_branch()

        data = []
        for i, branch in enumerate(self.git.branches()):
            br = str(branch)
            pushed = self.git.compare_hash(br)

            no_cleanup = br in cleanup_ignore

            state = self.__upstream_status__(br, pushed, main_br)
            br_ = self.__wrk_status__(br, main_br, cur, wrk, wrk_hist, no_cleanup)
            tasks = self.__tasks__(br)
            mark = " " + Fore.GREEN + RIGHT + Fore.RESET if cur == br else ""
            data.append([br_, state, tasks])

        print(tabulate(data, headers=["Branch", "State", "Tasks"]))
        print()
        print(
            Fore.GREEN + "Current" + Fore.RESET,
            Fore.BLUE + "Main" + Fore.RESET,
            Fore.CYAN + "Work" + Fore.RESET,
            Style.DIM + "Not work branch" + Style.RESET_ALL,
            "\x1B[4m" + "Ignore cleanup" + "\x1B[0m")
        print(
            PUSHED + " Sync w/ origin",
            UPSTREAM + " Has remote",
            NO_UPSTREAM + " No remote, not on " + Fore.BLUE + "Main" + Fore.RESET,
            MERGED + " Merged to " + Fore.BLUE + "Main" + Fore.RESET)

    def __tasks__(self, br):
        task_open_nr = len(self.tasks.get_tasks(br))
        task_done_nr = len(self.tasks.get_done_tasks(br))
        total = task_done_nr + task_open_nr
        if total == 0:
            return ""
        elif task_done_nr == 0:
            return "All done: " + str(total)
        else:
            return str(task_open_nr) + " of " + str(total)

    @staticmethod
    def __wrk_status__(br, main_br, checked, wrk, wrk_hist, no_cleanup):
        color = ""
        style = ""

        if br == wrk:
            color = Fore.CYAN
        elif br == checked:
            color = Fore.GREEN
        elif br == main_br:
            color = Fore.BLUE
        elif br not in wrk_hist:
            style = Style.DIM
        if no_cleanup:
            br = "\x1B[4m" + br + "\x1B[0m"

        return style + color + br + Style.RESET_ALL

    def __upstream_status__(self, branch, pushed, main_br):
        upstream = self.git.has_remote(branch)
        merged = self.git.is_merged(branch, main_br)

        state = ""
        if pushed:
            state = PUSHED
        elif upstream:
            state = UPSTREAM
        elif merged:
            state = LEFT
        else:
            state = NO_UPSTREAM
        return state
