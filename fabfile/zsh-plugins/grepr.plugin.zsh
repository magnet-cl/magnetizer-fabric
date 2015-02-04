# grep recursive through all
# Example:
#   grep --exclude=\*.{sh,py,js,css} -Ir "test" *

function grepr(){
    query=false
    params=()

    # go through all parametres, to separate parameters from the query
    # string
    for s in $*
    do
        case $s in 
            --django)
                params+="--exclude-dir=\.env"
                params+="--exclude-dir=node_modules"
                params+="--exclude-dir=bower_components"
                params+="--exclude-dir=fixtures"
                params+="--exclude-dir=CACHE"
                ;;
            --em)
                params+="--exclude-dir=migrations"
                ;;
            -*)
                # this is a parameter
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

    grep $params -Inr "$query" *
}
