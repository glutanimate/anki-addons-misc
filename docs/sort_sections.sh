#!/bin/bash
# Sorts markdown sections (default header level: ###)

if [[ ! -f "$1" ]]; then
    echo "No valid file provided."
    exit
fi

File="$1"
FileName="${File##*/}"
BaseName="${FileName%.*}"
DirName="${File%/*}"

Level="$2"

if [[ -z "$Level" ]]; then
    Level="###"
fi

perl -0777 -ne "
    (undef,@paragraphs) = split /^${Level}(?=[^${Level}])/m; 
    print map {\"${Level}\$_\"} sort @paragraphs;
" "$1" > "${FileName}_sorted.md"
