import os

NO = 0
YES = 1
CANCEL = 2


def confirm(question, cancelable=False):
    print(question)
    prompt = '(Yes/No/Cancel) << '
    if not cancelable:
        prompt = '(Yes/No) << '
    ans = input(prompt).lower()

    if ans in ['yes', 'y']:
        return YES
    elif ans in ['no', 'n']:
        return NO
    elif ans in ['cancel', 'c']:
        return CANCEL
    else:
        return CANCEL


def dedup(ls):
    seen = {}
    new_list = [seen.setdefault(x, x) for x in ls if x not in seen]
    return new_list


def is_valid_index(ls, index):
    return len(ls) > index


def is_nix():
    return os.name != 'nt'
