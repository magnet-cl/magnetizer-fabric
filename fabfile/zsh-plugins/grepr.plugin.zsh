# grep recursive through all
# Example:
#   grep --exclude=\*.{sh,py,js,css} -Ir "test" *

function grepr(){
    COUNT=1

    for s in $*
    do
        case $s in 
            -*)
                let COUNT+=1
                ;;
            *) 
                break
                ;; 
        esac
    done

    QUERY=${*: $COUNT}
    grep ${*: 1:$COUNT-1} -Inr "$QUERY" *
}
