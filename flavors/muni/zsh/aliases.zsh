alias g='git status'

function gpp(){
    set -e
    git smart-pull
    git push 
}

alias gup='git smart-pull'
alias grepd='grepr --django'

alias ltr='ls -ltr'
