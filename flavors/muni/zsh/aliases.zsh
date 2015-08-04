alias g='git status'

function gpp(){
    git smart-pull
    git push 
}

alias gup='git smart-pull'
alias grepd='grepr --django'
alias grepf='grepd --fu'

alias ltr='ls -ltr'
alias dj='python manage.py'
alias djr='./reset.sh'
alias djsh='dj shell'
alias djt='dj test'

function djrs() {
    ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{print $1}'
    ./reset.sh -s
}

function djs() {
    ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{print $1}'
    dj runserver 0.0.0.0:8000 --nothreading
}

function gpp(){
    git smart-pull
    git push 
}

alias piong='ping'
alias py='ipython'
alias reload=". ~/.zshrc && echo 'ZSH config reloaded from ~/.zshrc'"

function grm() {

    if [ $# -eq 0 ]
    then
        branch_name="$(git symbolic-ref HEAD 2>/dev/null)" ||
        branch_name="(unnamed branch)"     # detached HEAD
        branch_name=${branch_name##refs/heads/}
    else
        branch_name=$@
    fi
    
    git checkout $branch_name
    git fetch 
    git rebase origin/development
    git checkout development
    gup
    git merge $branch_name
    gup
    git push origin development
    git checkout $branch_name
}
