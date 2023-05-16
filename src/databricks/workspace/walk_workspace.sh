#!/bin/bash

# gets the original workspace root level folders
root=$(echo \'/\')
declare -a "folders=( $root )"
#
echo "folders: ${#folders[@]}"
x=1
z=1
while [ $x -le "${#folders[@]}" ]
do
    curr_index=$((x-1))
    curr_item="${folders[$curr_index]}"
    #curr_item=${curr_item//"'"/""}
    curr_return=$(databricks workspace list -l --absolute $curr_item)
    curr_grep=$(echo "${curr_return}" | grep -oP "(?<=DIRECTORY  ).*$" )
    #curr_arr=$("${curr_grep}" | sed -e  "s/\(.*\)/'\1'/")
    #curr_arr=$(echo $curr_arr | tr -d '\n' )
    SAVEIFS="$IFS"
    IFS=$'\n'
    for i in ${curr_grep[@]}
    do
            z=$((z+1))
            folders+=( "${i}" )
    done
    IFS="$SAVEFIFS"
    echo "folders: ${folders[@]}"

    #folders+=( ${curr_arr} )
    libraries+=$(echo "${curr_return}" | grep -oP "(?<=LIBRARY  ).*$")
    notebooks+=$(echo "${curr_return}" | grep -oP "(?<=NOTEBOOK  ).*$")
    files+=$(echo "${curr_return}" | grep -oP "(?<=FILE  ).*$")
    x=$((x+1))
done
