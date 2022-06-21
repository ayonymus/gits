from colorama import Fore, Style


class OverviewCli:    
    """
    Functions that use separate modules
    """

    def __init__(self, git, workbranch):
        self.workbranch = workbranch
        self.git = git
    
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

