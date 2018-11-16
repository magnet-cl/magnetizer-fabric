# grep recursive through all
# Example:
#   grep --exclude=\*.{sh,py,js,css} -Ir "test" *

function grepr(){
    fuzzy=false
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
                params+="--exclude=*.sql"
                params+="--exclude=*.log"
                ;;
            --em)
                params+="--exclude-dir=migrations"
                ;;
            --py)
                params+="--include=*.py"
                ;;
            --es)
                params+="--exclude-dir=static"
                ;;
            --ev)
                params+="--exclude-dir=vendor"
                ;;
            --fu)
                fuzzy=true
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

    if [ $fuzzy != false ] ; then
        query=$(echo $query | sed 's/\( \)/.*/g')
        echo $query
    fi

    grep $params -Inr "$query" *
}
