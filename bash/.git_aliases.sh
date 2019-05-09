#!/bin/bash

## regular git commands
alias add="git add"
alias adda="git add ."
alias br="git branch"
alias com="git commit"
alias coma="git commit --amend"
alias coman="git commit --amend --no-edit"
alias comm="git commit -m"
alias cur="git rev-parse --abbrev-ref HEAD" # name of current branch
alias f="git fetch"
alias logs="git log --oneline"
alias pull="git pull"
alias push="git push"
alias stat="git status"
alias stash="git stash"

## chained git commands
alias stasha="git add . && git stash"                   # stash all current changes including untracked files

# push current branch to remote server
upstream() {
	git push --set-upstream origin $(cur)
}
