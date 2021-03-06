# gits

A collection of scripts to simplify some of everyday tasks while working with `git` in a collaborative environment.


## Usage
Make sure you have `python 3` and `gitpython` installed.

Clone the project to your __linux__ or __mac__ machine, and create an `alias` to `.gits.py`.
Alternatively, for easier use, make an alias to `bash/.gits_aliases` that already has a few short cuts.

Run `.gits.py` and see the available options.

Some extra information about your work is stored in your project's `.git` folder.


## Features
This is not a comprehensive list of all functsions. The `--help` fairly well describes each function.
To see the list of features:

`gits.py`

Feature help:
`gits.py {feature} -h`

### checkout
Forwards commands to `git checkout`, but also saves the checkout target to a list.

To view the history: 
`gits.py checkout -H`

To check out a branch from the history:
`gits.py checkout -bh {branch id}`

### work
Mark a branch as "work branch" so that it's easy to get back to it when you are working with multiple branches.

Suppose you work on branch `ticket-1234-killer_feature`, but you have to check out `ticket-1236-weird_bug` branch for review:

```
## sets current branch 'ticket-1234-killer_feature' as a work branch
gits.py work -s 			

## review code on another branch
gits.py checkout ticket-1236-weird_bug

## you don't have to find what branch you were working on, just check out
gits.py work -c
```

As an extra, you also have a work history, could come handy at perfomance reviews.

### task
Light weight 'todo list'. Assign a `task` to any branch, review when done.

### cleanup
Sometimes you end up with lots of branches checked out, making it hard to know what's going on with them.
This tool helps to clean them up. Must run from 'development' or 'master' branch.

Before deleting, the script checks if:
* the branch is merged to 'development' or 'master' branch (i.e. the current checked out branch)
* has open tasks
* is branch on white list
* delete is confirmed in a prompt

The most powerful feature is the `--iterate` flag, which iterates over all the local branches and calls the `cleanup` function.
Unmerged branches are left intact, those have to be removed manually.

The white list is editable.


Bug reports, pull requests are welcome!



