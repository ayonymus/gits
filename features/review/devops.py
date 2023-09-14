
import requests

from data.models import Devops
from data.store import Storage2
from tools.githelper import GitHelper

AZURE = "azure"
GITHUB = "github"


class DevOpsStore:

    def __init__(self, store: Storage2):
        self.store = store

    def load_devops(self):
        model = self.store.load_model()
        print(model.notes)
        devops = self.store.load_model().devops
        return devops

    def store_devops(self, devops: Devops):
        data = self.store.load_model()
        data.devops = devops
        self.store.store_model(data)


class DevOpsHandler:

    def __init__(self, store: Storage2, git: GitHelper):
        self.store = DevOpsStore(store)
        self.git = git

    def configure(self, provider, token):
        if provider == AZURE:
            self.__configure_azure__(token)
        elif provider == GITHUB:
            self.__configure_github__(token)
        else:
            print("Invalid argument")
            exit(1)

    def __configure_azure__(self, token):
        # TODO already set?
        # TODO validate expected url?
        remote = self.git.get_origin_url()
        project_url, repo_name = remote.split('_git/')
        pr_url = project_url + '_apis/git/repositories/' + repo_name + '/pullrequests?api-version=7.0'
        configs = {'pr_url': pr_url,
                   'url': project_url,
                   'repo_name': repo_name,
                   'token': token}

        devops = Devops()
        devops.provider = AZURE
        devops.config = configs
        self.store.store_devops(devops)
        print(f'Project url: {project_url}')
        print(f'Repository name: {repo_name}')

    def __configure_github__(self, token):
        remote = self.git.get_origin_url()
        github, repo = remote.split(':')
        config = {
            'repo': repo.removesuffix('.git'),
            'token': token
        }
        devops = Devops()
        devops.provider = GITHUB
        devops.config = config
        self.store.store_devops(devops)
        print(f"Repository name: {config['repo']}")

    def get_prs(self):
        devops = self.store.load_devops()
        # TODO not configured yet?
        if devops.provider == AZURE:
            return self.__get_azure_prs__(devops.config)
        if devops.provider == GITHUB:
            return self.__get_github_prs__(devops.config)
        else:
            return None

    def __get_azure_prs__(self, config):
        pat = config['token']
        response = requests.get(url=config['pr_url'], auth=(pat))
        web_url = config['url']
        repo_name = config['repo_name']
        if response.status_code == 200:
            results = []
            for pr in response.json()['value']:
                id = pr['pullRequestId']
                url = f'{web_url}/_git/{repo_name}/pullrequest/{id}'
                results.append((pr['title'],
                                pr['sourceRefName'].replace('refs/heads/', ''),
                                pr['targetRefName'].replace('refs/heads/', ''),
                                pr['mergeStatus'],
                                pr['creationDate'],
                                url))
            return results
        elif response.status_code != 401:
            print("401: Personal access token not accepted.")
            exit(1)
        else:
            print("Unexpected response")
            exit(1)

    def __get_github_prs__(self, config):
        pat = config['token']
        url = ('https://api.github.com/repos/%s/%s' % (config['repo'], 'pulls'))
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + pat,
            "X-Github-Api-Version": "2022-11-28"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            results = []
            for pr in response.json():
                results.append((pr['title'],
                                pr['head']['ref'],
                                pr['base']['ref'],
                                pr['state'],
                                pr['created_at'],
                                pr['html_url']))
            return results

        elif response.status_code != 401:
            print("401: Personal access token not accepted.")
            exit(1)
        else:
            print("Unexpected response")
            exit(1)