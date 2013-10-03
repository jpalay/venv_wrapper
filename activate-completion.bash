_activate_show()
{
        local cur

        COMPREPLY=()
        cur=${COMP_WORDS[COMP_CWORD]}
        COMPREPLY=($( compgen -W "$(for x in `lsvenv`; do echo $(basename ${x}); done)" -- $cur ) )
}
complete -F _activate_show activate
complete -F _activate_show rmvenv
