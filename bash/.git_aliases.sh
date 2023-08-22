#!/bin/bash

DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

export GITS_HOME="$(dirname "$DIR")"

alias gita="cat $DIR/.git_aliases.sh"

## regular git commands
alias add="git add"
alias adda="git add ."
alias br="git branch --sort=-committerdate"
alias com="git commit"
alias coma="git commit --amend"
alias coman="git commit --amend --no-edit"
alias comm="git commit -m"
alias comn="git commit --no-verify -m"
alias cur="git rev-parse --abbrev-ref HEAD" # name of current branch
alias f="git fetch"
alias logs="git log --oneline"
alias pull="git pull"
alias push="git push"
alias stat="git status"
alias stash="git stash"

# push current branch to remote server
upstream() {
	git push --set-upstream origin $(cur)
}

# find remote branch by name
findbr() {
	git branch -r |grep $1
}