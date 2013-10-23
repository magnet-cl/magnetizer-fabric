# cd + virtualenv activation + ls
function cd() {
    # default cd
    builtin cd $1;

    # virtualenv activation
    GIT_DIR=`git rev-parse --git-dir 2> /dev/null`
    if [[ $? == 0 ]]
    then
        if [[ -f $GIT_DIR/../.env/bin/activate ]]
        then
            . $GIT_DIR/../.env/bin/activate
        else
            if [[ $VIRTUAL_ENV != "" ]]
            then
                deactivate
            fi
        fi
    else
        if [[ $VIRTUAL_ENV != "" ]]
        then
            deactivate
        fi
    fi

    # optional ls
    ls
}
