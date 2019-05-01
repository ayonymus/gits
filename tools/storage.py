
import json

KEY_BRANCH = 'workbranches'
KEY_TASK = 'tasks'

PATH_STORAGE = "/.git/gits"


class Storage:
    # TODO implement some caching

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
        return self.__get_works__(self.__load__())

    def __get_works__(self, data):
        try:
            return data[KEY_BRANCH]
        except:
            return []

    def update_branch_history(self, branch_list):
        data = self.__load__()
        data[KEY_BRANCH] = branch_list
        self.__store__(data)

    # tasks
    def load_all_tasks(self):
        return self.__get_tasks__(self.__load__())

    def __get_tasks__(self, data):
        try:
            return data[KEY_TASK]
        except:
            return dict()

    def store_tasks(self, tasks):
        data = self.__load__()
        data[KEY_TASK] = tasks
        self.__store__(data)
