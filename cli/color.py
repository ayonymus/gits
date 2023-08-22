from termcolor import colored

CURRENT = 'green'
MAIN = 'blue'
WORK = 'cyan'
DELETED = 'red'
REVIEW = 'magenta'

Current = colored('Current', CURRENT)
Main = colored('Main', MAIN)
Work = colored('Work', WORK)
Important = "\x1B[4m" + "Important" + "\x1B[0m"
Deleted = colored('[Deleted]', DELETED)
Review = colored("[Review]", REVIEW)


def current(branch): return colored(branch, CURRENT)


def main_(branch): return colored(branch, MAIN)


def work(branch): return colored(branch, WORK)


def important(branch): return "\x1B[4m" + branch + "\x1B[0m"


def deleted(branch): return colored(branch, DELETED)


def error(msg): return colored(msg, 'red')


def warn(msg): return colored(msg, 'yellow')


def gray(msg): return colored(msg, 'gray')


def review(msg): return colored(msg + ' [Review] ', REVIEW)


def apply_color(branch, tags, is_deleted, curr=None):
    if is_deleted:
        return deleted(branch)
    if tags.main is not None and branch == tags.main:
        if branch == curr:
            return main_(branch) + current(' [Current] ')
        else:
            return main_(branch)
    if tags.work is not None and branch == tags.work[0]:
        return work(branch)
    if tags.important is not None and branch in tags.important:
        return important(branch)
    if branch == curr:
        return current(branch)
    return branch


def __showcase_palette__():
    print(Current)
    print(Main)
    print(Work)
    print(Important)
    print(Deleted)
    print(Review)


def main():
    __showcase_palette__()


if __name__ == '__main__':
    main()
