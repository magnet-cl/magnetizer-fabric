# find files by name using find -name
# Example:
#   findm --exclude=\*.{sh,py,js,css} -Ir "test" *

function findm(){
    query=false
    exclude=()
    look_for_extension=false

    # go through all parametres, to separate parameters from the query
    # string
    for s in $*
    do
        case $s in 
            --django)
                exclude+="-not -path \"./.env/*\""
                exclude+='-not -path "./node_modules/*"'
                exclude+='-not -path "./base/static/bower_components/*"'
                exclude+='-not -path "./fixtures/*"'
                exclude+='-not -path "./CACHE/*"'
                ;;
            -e)
                look_for_extension=true
                ;;
            -*)
                # this is a parameter for grepr
                params+=$s
                ;;
            *) 
                if [ $query = false ] ; then
                    query="$s"
                else
                    query="$query $s"
                fi
                ;; 
        esac
    done

    if [ $look_for_extension=false ] ; then
        eval "find .  $params -name \"$query*\" $exclude"
    else
        eval "find .  $params -name \"*.$query\" $exclude"
    fi
}
