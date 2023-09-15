# gits

A command line tool for simplifying collaboration with others. Tested on Linux, Mac and Windows.

It is mostly geared at working with multiple branches and simplifying the code review process.


## Problem Statement
Working in a high performance, very collaborative team comes with its own set of problems.
Imagine you have a `main` branch and are working on a feature on `feature/newfeature`. A higher priority task comes in.
You start working on it on `task/priority_task`. Now a bug comes in, and you do a quick fix on 
`bug/fixing`. You also want to check out a branch to review a pull request more thoroughly. 

Now you end up with 5 different branches on your local repository, and you have to figure out what were you working on.

By using the `gits` script you can ease this problem.

## Overview
`gits --overview` gives a glance the status of all your local branches.

## checkout
Using `gits checkout <branch>` command instead of regular `git checkout` will also keep a log 
of checked out branches in a more readable format than `git reflog`.
You can also check out a branch from this branch log.

You can also easily switch to special marked branches (`work` and `main`).

## marked branches

Currently, there are 3 markers handled:

### main
Mark the most important branch as main.
 
### work

###important




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



