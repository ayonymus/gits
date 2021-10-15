
import json

KEY_BRANCH = 'workbranches'
KEY_TASK = 'tasks'
KEY_TASK_DONE = 'tasks_done'

KEY_CHECKOUT_HISTORY = 'checkouts'

KEY_CLEANUP_MAIN_BARNCHES = 'main_branch'
KEY_CLEANUP_IGNORED_BRANCHES = 'cleanup_branch_ignore_list'

PATH_STORAGE = "/.git/gits"


class Storage:

    __storage_file__ = None

    def __init__(self, path):
        self.__storage_file__ = path + PATH_STORAGE

    def __store__(self, data):
        with open(self.__storage_file__, 'w') as json_file:
            return json.dump(data, json_file)

    def __load__(self):
        try:
            with open(self.__storage_file__, 'r') as json_file:
                return json.loads(json_file.read())
        except FileNotFoundError:
            return {}

    # work branch
    def load_work_branches(self):
        return self.__get_list__(self.__load__(), KEY_BRANCH)

    def __get_list__(self, data, key):
        try:
            return data[key]
        except:
            return []

    def __get_dict__(self, data, key):
        try:
            return data[key]
        except:
            return {}

    def update_branch_history(self, branch_list):
        data = self.__load__()
        data[KEY_BRANCH] = branch_list
        self.__store__(data)

    # tasks
    def load_all_tasks(self):
        return self.__get_dict__(self.__load__(), KEY_TASK)

    def store_tasks(self, tasks):
        data = self.__load__()
        data[KEY_TASK] = tasks
        self.__store__(data)

    def load_all_done_tasks(self):
        return self.__get_dict__(self.__load__(), KEY_TASK_DONE)

    def store_done_tasks(self, tasks):
        data = self.__load__()
        data[KEY_TASK_DONE] = tasks
        self.__store__(data)

    # checkout history
    def load_checkout_history(self):
        try:
            return self.__load__()[KEY_CHECKOUT_HISTORY]
        except:
            return None

    def store_checkout_history(self, branch_list):
        data = self.__load__()
        data[KEY_CHECKOUT_HISTORY] = branch_list
        self.__store__(data)

    # cleanup
    def load_main_branches(self):
        try:
            return self.__load__()[KEY_CLEANUP_MAIN_BARNCHES]
        except:
            return []

    def store_main_branch(self, main_list):
        data = self.__load__()
        data[KEY_CLEANUP_MAIN_BARNCHES] = main_list
        self.__store__(data)

    def load_cleanup_whitelist(self):
        try:
            return self.__load__()[KEY_CLEANUP_IGNORED_BRANCHES]
        except:
            return []

    def store_cleanup_whitelist(self, white_list):
        data = self.__load__()
        data[KEY_CLEANUP_IGNORED_BRANCHES] = white_list
        self.__store__(data)
