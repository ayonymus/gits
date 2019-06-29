
def confirm(question):
    print(question)
    ans = input('(Y/N) << ').lower()
    if ans in ['yes', 'y']:
        return True
    if ans in ['no', 'n']:
        return False
