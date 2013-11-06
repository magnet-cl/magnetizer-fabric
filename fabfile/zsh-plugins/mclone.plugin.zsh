# git clone for github.com/magnet-cl repositories
# Example:
#   mclone magnetizer

function mclone(){
    BITBUCKET_CLONE=true
    GITHUB_CLONE=false

    while [ "$1" != "" ]; do
        case $1 in
            -g | --github )
                BITBUCKET_CLONE=false
                GITHUB_CLONE=true
                ;;
        esac
        shift
    done

    if $GITHUB_CLONE ; then
        echo "Cloning from github"
        git clone git@github.com:magnet-cl/$1.git
    else
        echo "Cloning from bitbucket"
        git clone git@bitbucket.org:magnet-cl/$1.git
    fi
}
