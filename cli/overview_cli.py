from colorama import Fore, Style
from tabulate import tabulate


RIGHT="\u25b6"
UP="\u25b2"
LEFT="\u25c0"
DOWN="\u25bc"

PUSHED = Fore.GREEN + UP + Fore.RESET
MERGED = LEFT
NOT_PUSHED = Fore.RED + UP + Fore.RESET

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

        data =[]
        for i, branch in enumerate(self.git.branches()):
            br = str(branch)
            task_nr = len(self.tasks.get_tasks(br))
            task_done_nr = len(self.tasks.get_done_tasks(br))
            no_cleanup = br in cleanup_ignore

            state = self.__upstream_status__(br, main_br)
            br_ = self.__wrk_status__(br, main_br, checked, wrk, wrk_hist, no_cleanup)
            tasks = self.__tasks__(br)

            data.append([br_, state, tasks])

        print(tabulate(data, headers=["Branch", "State", "Tasks"]))
        print()
        print(
        	Fore.GREEN + "Current" + Fore.RESET, 
        	Fore.BLUE + "Main" + Fore.RESET, 
        	Fore.CYAN + "Work" + Fore.RESET, 
        	Style.DIM + "Not work branch" + Style.RESET_ALL,
        	"\x1B[4m" + "Don't clean up" + "\x1B[0m")
        print("Pushed: ", PUSHED, "Not pushed: ", NOT_PUSHED, "Merged to main: " + MERGED)

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

    def __wrk_status__(self, br, main_br, checked, wrk, wrk_hist, no_cleanup):
        color = Style.DIM
        if br in wrk_hist:
            color = Fore.WHITE
        if br == wrk:
            color = Fore.CYAN
        if br == checked:
            color = Fore.GREEN
        if br == main_br:
            if br == checked:
                color = Fore.GREEN
            else:
                color = Fore.BLUE
        if no_cleanup:
        	br = "\x1B[4m" + br + "\x1B[0m"
        return color + br + Style.RESET_ALL


    def __upstream_status__(self, branch, main_br):
        pushed = self.git.has_remote(branch)
        merged = self.git.is_merged(branch, main_br)

        state = ""
        if pushed:
            state = PUSHED
        elif merged:
        	state = LEFT
        else:
            state = NOT_PUSHED
        return state







