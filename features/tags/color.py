from termcolor import colored

CURRENT = 'green'
MAIN = 'blue'
WORK = 'cyan'
DELETED = 'red'

Current = colored('Current', CURRENT)
Main = colored('Main', MAIN)
Work = colored('Work', WORK)
Important = "\x1B[4m" + "Important" + "\x1B[0m"
Deleted = colored('[Deleted]', DELETED)


def current(branch): return colored(branch, CURRENT)


def main(branch): return colored(branch, MAIN)


def work(branch): return colored(branch, WORK)


def important(branch): return "\x1B[4m" + branch + "\x1B[0m"


def deleted(branch): return colored(branch, DELETED)


def error(msg): return colored(msg, 'red')