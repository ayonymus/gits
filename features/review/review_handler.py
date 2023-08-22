from features.tags.tags import TagsHandler
from tools.githelper import GitHelper


class ReviewHandler:

    def __init__(self, git: GitHelper, tags: TagsHandler):
        self.git = git
        self.tags = tags

    def get_remotes(self):
        self.git.fetch()
        return self.git.remote_branches()


def main():
    handler = ReviewHandler(
        git=GitHelper(),
        tags=None
    )
    handler.get_remotes()
    print(handler.git.remotes())
    print(handler.git.branches())
    print(handler.git.branches_str())


if __name__ == '__main__':
    main()
