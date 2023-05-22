#!/bin/bash

# function file_path() {
#     path_root="${1}"
#     filepart="${2}"

#     [ "${path_root}" == "" ] && path_root=$(pwd)

#     # test whether dir or file
#     if [ -d "$path_root" ]
#     then
#         abspath="$(realpath "$path_root")/"
#     else
#         abspath="$(realpath "$path_root")"
#     fi

#     file="${abspath##*/}"
#     dir="${abspath:0:${#abspath} - ${#file}}"
#     #folder="$(basename $(dirname "$abspath"))"
#     folder=$(basename "${dir}")
#     base="${file%.[^.]*}"
#     ext="${file:${#base} + 1}"

#     if [[ -z "$base" && -n "$ext" ]]
#     then
#         base=".$ext"
#         ext=""
#     fi

#     all="|| abspath: ${abspath} | dir: ${dir} | folder: ${folder} | file: ${file} | base: ${base} | ext: ${ext} ||"

#     echo "${!filepart}"
# }

# defaults to current directory
path_root="${1}"
[ "${path_root}" == "" ] && path_root=$(pwd)

 # test whether dir or file
if [ -d "$path_root" ]
then
    abspath="$(realpath "$path_root")/"
else
    abspath="$(realpath "$path_root")"
fi


find "${abspath}" -type f -exec sh -c '
  for file do
    file_old="${file##*/}"
    dir="$(dirname ${file})"
    file_new=$(echo ${file_old} | tr -s " " "_")
    file_new=$(echo "${file_new}" | tr "A-Z" "a-z")
    file_new=$(echo "${file_new}" | tr "-" "_")
    if [ "${file_old}" != "${file_new}" ]
    then
                echo "moving ${dir}/${file_old} >>  ${dir}/${file_new}"
        mv "${dir}/${file_old}" "${dir}/${file_new}"
    fi

  done
' exec-sh {} +

find "${abspath}" -type f -exec chmod 775 {} \;


