NO = 0
YES = 1
CANCEL = 2

def confirm(question, cancelable):
    print(question)
    prompt = '(Yes/No/Cancel) << '
    if not cancelable: 
        prompt = '(Yes/No) << '
    ans = input(prompt).lower()
    
    if ans in ['yes', 'y']:
        return YES
    if ans in ['no', 'n']:
        return NO
    if ans in ['cancel', 'c']:
        return CANCEL
