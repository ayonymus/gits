from features.review.devops import DevOpsHandler
from features.tags.tags import TagsHandler
from tools.githelper import GitHelper


class ReviewHandler:

    def __init__(self, git: GitHelper, tags: TagsHandler, devops: DevOpsHandler):
        self.git = git
        self.tags = tags
        self.devops = devops

    def get_remotes(self):
        self.git.fetch()
        return self.git.remote_branches()

    def get_prs(self):
        return self.devops.get_prs()


def main():
    handler = ReviewHandler(
        git=GitHelper(),
        tags=None
    )


if __name__ == '__main__':
    main()
