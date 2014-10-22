# grep recursive through all
# Example:
#   grep --exclude=\*.{sh,py,js,css} -Ir "test" *

function grepr(){
    query=""
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
                ;;
            -*)
                # this is a parameter
                params+=$s
                ;;
            *) 
                query="$query $s"
                ;; 
        esac
    done

    grep $params -Inr "$query" .
}
