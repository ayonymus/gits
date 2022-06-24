from colorama import Fore, Style
from tabulate import tabulate

class OverviewCli:    
    """
    Functions that use separate modules
    """

    def __init__(self, git, workbranch, tasks, branch_cleanup):
        self.workbranch = workbranch
        self.git = git
        self.tasks = tasks
        self.cleanup = branch_cleanup
    
    def print_branches(self):
        wrk = str(self.workbranch.get_work_branch())
        wrk_hist = self.workbranch.get_work_branch_history()
        checked = str(self.git.branch())
        for i, branch in enumerate(self.git.branches()):
            br = str(branch)
            color = Style.DIM
            state = ""
            if br in wrk_hist:
                color = Fore.WHITE
            if br == wrk:
                state = Fore.CYAN + " (work)"
                color = Fore.CYAN
            if br == checked:
                color = Fore.GREEN
            print(color + br + state + Style.RESET_ALL)


    def print_overview(self):
        wrk = str(self.workbranch.get_work_branch())
        wrk_hist = self.workbranch.get_work_branch_history()
        checked = str(self.git.branch())
        cleanup_ignore = self.cleanup.get_ignorelist()
        main_br = self.cleanup.get_main_branch()

        data = []

        for i, branch in enumerate(self.git.branches()):
            br = str(branch)
            task_nr = len(self.tasks.get_tasks(br))
            task_done_nr = len(self.tasks.get_done_tasks(br))
            no_cleanup = br in cleanup_ignore
            
            pushed = self.git.has_remote(br)
            merged = self.git.is_merged(br, main_br)

            color = Style.DIM
            state = ""

            if br in wrk_hist:
                color = Fore.WHITE
            if br == wrk:
                state = Fore.CYAN + " (work)"
                color = Fore.CYAN
            if br == checked:
                color = Fore.GREEN
            if br == main_br:
                state = Fore.BLUE + " (main)"
                if br == checked:
                    color = Fore.GREEN
                else:
                    color = Fore.BLUE
            data.append([color + br + state + Style.RESET_ALL, task_nr, task_done_nr, no_cleanup, pushed, merged])
        print(tabulate(data, headers=["Branch", "Open tasks", "Done tasks", "Don't clean up", "Pushed", "Merged to main"]))

