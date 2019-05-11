#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

export GITS_HOME="$(dirname "$DIR")"

alias gitsa="cat $DIR/.gits_aliases.sh"

# Aliases for gits
alias gits="$GITS_HOME/gits.py"

alias ch="$GITS_HOME/gits.py checkout"

alias work="$GITS_HOME/gits.py work"

alias tsk="$GITS_HOME/gits.py task"
