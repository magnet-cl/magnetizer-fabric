# cd + virtualenv activation + ls
function cd() {
    # default cd
    builtin cd $1;

    # virtualenv activation
    GIT_DIR=`git rev-parse --git-dir 2> /dev/null`
    if [[ $? == 0 ]]
    then
        if [[ -f $GIT_DIR/../Pipfile ]]
        then
            if [[ $PIPENV_ACTIVE != "1" ]]
            then
                if [[ $VIRTUAL_ENV != "" ]]
                then
                    deactivate
                fi

                VENV=`pipenv --venv`

                . $VENV/bin/activate
                # pipenv shell
            fi
        else
            if [[ $PIPENV_ACTIVE == "1" ]]
            then
                exit
            fi
            if [[ -f $GIT_DIR/../.env/bin/activate ]]
            then
                . $GIT_DIR/../.env/bin/activate
            else
                if [[ $VIRTUAL_ENV != "" ]]
                then
                    deactivate
                fi
            fi
        fi
    else
        if [[ $VIRTUAL_ENV != "" ]]
        then
            if [[ $PIPENV_ACTIVE == "1" ]]
            then
                CURRENT_FOLDER=PWD
                exit
            else
                deactivate
            fi
        fi
    fi

    # optional ls
    ls
}
