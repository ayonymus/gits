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


## Main Features
### Overview
`gits --overview` gives a glance the status of all your local branches, ordered by most recent commit.

![overview.png](docs%2Foverview.png)

### checkout
Using `gits checkout <branch>` command instead of regular `git checkout` will also keep a log 
of checked out branches in a more readable format than `git reflog`.
You can also check out a branch from this branch log.

You can also easily switch to special marked branches (`work` and `main`).

### mark 
Association branches with certain markers can help you to easily switch back and forth between various branches.
Also, the marked branches will be ignored during cleanup.
Currently, there are 3 special markers that are handled:

#### main
Mark the most important branch as main.

`gits checkout -m` will check out the main branch
 
#### work
Mark the branch you are working on. This enables you to find what were you working on
when you had to move away to do something else

`gits checkout -w` will check out the current work branch

The list of work branches may also come in handy when you want to review what have you been working on in the past.

#### important
Mark an important branch.

### cleanup
With the cleanup feature you can prevent accidental deletions and data loss. Before deleting the branch the script checks if:
- branch is merged to main
- branch has unpushed changes to a remote branch
- has some gits notes associated
- is marked as main, work or important

#### iterate
Multiple branches could be deleted with the `--iterate` flag. With this command the script will walk through
all the local branches and prompt if you really want to delete a branch.

### notes
A lightweight note taking feature. You may associate notes or todos with a certain branch.

This is not a comprehensive list, but these are the most important ones. 

Note, this is a work in progress tool. Use at your own risk.


