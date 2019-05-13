#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

export GITS_HOME="$(dirname "$DIR")"

alias gita="cat $DIR/.git_aliases.sh"

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
# stash all current changes
alias stasha="git add . && git stash"

# push current branch to remote server
upstream() {
	git push --set-upstream origin $(cur)
}