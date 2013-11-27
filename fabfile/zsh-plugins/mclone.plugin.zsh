# git clone for github.com/magnet-cl repositories
# Example:
#   mclone magnetizer

function mclone(){
    GITHUB_CLONE=false

    usage() { echo "usage: mclone [-g] REPOSITORY [DIRECTORY]";}

    local OPTIND

    while [[ $# -gt 0 ]] ; 
    do
        if  [[ ."$1" = .-* ]] ; then 
            while getopts "g" o; do
                case "${o}" in
                    g)
                        echo "$OPTARG"
                        GITHUB_CLONE=true
                        ;;
                    *)
                        usage
                        return;
                        ;;
                esac
            done
        else
            REPOSITORY=$1
            DIRECTORY=$2
            # TODO This no longer allows for parameters to be on any order
            break
        fi
        shift
    done

    if $GITHUB_CLONE ; then
        echo "Cloning from github"
        command="git clone git@github.com:magnet-cl/$REPOSITORY.git $DIRECTORY"   
        echo $command
        eval $command
    else
        echo "Cloning from bitbucket"
        command="git clone git@bitbucket.org:magnet-cl/$REPOSITORY.git $DIRECTORY"
        echo $command
        eval $command
    fi
}
