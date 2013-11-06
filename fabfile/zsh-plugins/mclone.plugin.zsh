# git clone for github.com/magnet-cl repositories
# Example:
#   mclone magnetizer

function mclone(){
    GITHUB_CLONE=false

    usage() { echo "usage: mclone [-g] REPOSITORY";}

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
        fi
        shift
    done

    if $GITHUB_CLONE ; then
        echo "Cloning from github"
        echo "git clone git@github.com:magnet-cl/$REPOSITORY.git"
        git clone git@github.com:magnet-cl/$REPOSITORY.git
    else
        echo "Cloning from bitbucket"
        echo "git clone git@bitbucket.org:magnet-cl/$REPOSITORY.git"
        git clone git@bitbucket.org:magnet-cl/$REPOSITORY.git
    fi
}
