#!/bin/bash
path_root="${1}"
filepart="${2}"

[ "${path_root}" == "" ] && path_root=$(pwd) 

# test whether dir or file
if [ -d "$path_root" ]
then
    abspath="$(realpath "$path_root")/"
else
    abspath="$(realpath "$path_root")"
fi

file="${abspath##*/}"
dir="${abspath:0:${#abspath} - ${#file}}"
#folder="$(basename $(dirname "$abspath"))"
folder=$(basename "${dir}")
base="${file%.[^.]*}"
ext="${file:${#base} + 1}"

if [[ -z "$base" && -n "$ext" ]]
then
    base=".$ext"
    ext=""
fi

all="|| abspath: ${abspath} | dir: ${dir} | folder: ${folder} | file: ${file} | base: ${base} | ext: ${ext} ||"

echo "${!filepart}"
