
class TaskHandler:

    def __init__(self, storage):
        self.storage = storage

    def assign_task(self, branch, task):
        all_tasks = self.storage.load_all_tasks()
        if branch in all_tasks.keys():
            branch_tasks = all_tasks[branch]
            branch_tasks.append(task)
            all_tasks[branch] = branch_tasks
        else:
            all_tasks[branch] = [task]
        self.storage.store_tasks(all_tasks)

    def get_tasks(self, branch):
        all_tasks = self.storage.load_all_tasks()
        if branch in all_tasks.keys():
            return all_tasks[branch]
        else:
            return []
