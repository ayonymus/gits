

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

    def get_all_tasks(self):
        return self.storage.load_all_tasks()

    def get_tasks(self, branch):
        return self.__get_list__(self.get_all_tasks(), branch)

    def remove_task(self, branch, index):
        all_tasks = self.storage.load_all_tasks()
        tasks = self.__get_list__(all_tasks, branch)
        if len(tasks) > 0 and len(tasks) > index:
            tasks.pop(index)
            all_tasks[branch] = tasks
            self.storage.store_tasks(all_tasks)
            return True
        else:
            return False

    def get_done_tasks(self, branch):
        all_done_tasks = self.storage.load_all_done_tasks()
        return self.__get_list__(all_done_tasks, branch)

    def remove_done_tasks(self, branch):
        all_done_tasks = self.storage.load_all_done_tasks()
        if branch in all_done_tasks.keys():
            all_done_tasks.pop(branch)
            self.storage.store_done_tasks(all_done_tasks)

    def __get_list__(self, dictionary, key):
        if key in dictionary.keys():
            return dictionary[key]
        else:
            return []

    def set_task_done(self, branch, index):
        tasks = self.get_tasks(branch)
        if len(tasks) > index:
            done_task = tasks.pop(index)

            self.remove_task(branch, index)

            all_done_tasks = self.storage.load_all_done_tasks()

            branch_done = self.__get_list__(all_done_tasks, branch)
            branch_done.append(done_task)

            all_done_tasks[branch] = branch_done

            self.storage.store_done_tasks(all_done_tasks)
            return True
        return False

    def move_task(self, branch, old_pos, new_pos):
        all_tasks = self.storage.load_all_tasks()
        tasks = self.__get_list__(all_tasks, branch)
        if len(tasks) > old_pos and len(tasks) > new_pos:
            task = tasks.pop(old_pos)
            tasks.insert(new_pos, task)
            all_tasks[branch] = tasks
            self.storage.store_tasks(all_tasks)
            return True
        else:
            return False
