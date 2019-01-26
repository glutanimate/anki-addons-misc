#!/bin/bash
# Buildscript for add-ons in glutanimate/anki-addons-misc
#
# Builds and prepares files for upload to AnkiWeb
#
# Compatible add-on structures:
#
# 1.) single-file add-on
#
#   folder: addon_basename
#      →  file: __init__.py
#      →  file: addon_basename.py
#      → ?folder: docs
#
# 2.) multi-file 2.1-only add-on
#
#   folder: addon_basename
#      →  file: __init__.py
#      → ?file(s): *.py
#      → ?folder: docs
#
# 3.) multi-file add-on
#
#   folder: addon_basename
#      →  file: "Display Name.py"
#      →  folder: module_name
#           → file: __init__.py
#           → ...
#      → ...
#
# Copyright: (c) 2017-2018 Glutanimate <https://glutanimate.com/>
# License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>


set -ue

# Options
excluded_patterns=("*__pycache__/*" "meta.json" "*.pyc" "*.pyo" "*.html"
                   ".python-version" ".hidden" ".directory" "*.vscode/*" "*docs/*")
ALL="true"  # default: process all add-ons

# Global variables
wd_path="$PWD"
src_path="${wd_path}/src"
build_path="${wd_path}/build"
dist20_path="${build_path}/dist20"
dist21_path="${build_path}/dist21"


USAGE="
    ${0} [-afh] [<add-on basename>]

    Options:
        -a:           Build all add-ons [default if no other option provided]
        -f <names>:   Build add-ons that are passed in a space-separated list
                      directory name inside the src folder
        -h:           show this help section
"


# evaluate options
while getopts "afh" OPTIONS; do
  case $OPTIONS in
    a ) ALL="true"
        ;;
    f ) ALL="false"
        ;;
    h ) echo "Usage: $USAGE"
        exit 0
        ;;
   \? ) echo "$USAGE"
        exit 1
        ;;
  esac
done
# remove options from arguments after processing is done
shift $((OPTIND-1))


build_all () {
    echo -e "Building all 'anki-addons-misc' add-ons...\n"
    # Safely iterate over src directories and call build_addon()
    while IFS= read -d $'\0' -r addon_dir ; do
        base=$(basename "${addon_dir}")
        build_addon "${base}"
    done < <(find "${src_path}" -mindepth 1 -maxdepth 1 -type d -print0)
}

build_specific () {
    echo -e "Building the following add-on(s): $@\n"
    for addon in "$@"; do
        build_addon "$addon"
    done
}


build_addon () {
    addon="$1"

    if [[ -z "${addon}" || -z "${src_path}" ]]; then
        echo "No add-on or source path supplied. Aborting."
        exit 1
    fi

    cd "${src_path}/${addon}"

    echo "Building ${addon} for Anki 2.0 and 2.1..."
    # Determine whether we're dealing with a single-file or multi-file add-on
    if [[ -f "__init__.py" ]]; then  # single-file add-on
        if [[ -f "${addon}.py" ]]; then
            # Anki 2.0:
            cp "${addon}.py"  "${dist20_path}/"
        fi
        # Anki 2.1:
        zip -FS -r $exclude_string "${dist21_path}/${addon}.zip" *
    else
        # find entry file for importing module into Anki 2.0
        entry_file=$(find . -mindepth 1 -maxdepth 1 -type f -name "*.py")
        # find module directory by looking at dirs containing initfile
        module_dir=$(find . -mindepth 2 -maxdepth 2 -name __init__.py -print0 | \
                     xargs -0 -n1 dirname | sort --unique)
        if [[ -z "$entry_file" || -z "$module_dir" || $(echo "$entry_file" | wc -l) != 1 || $(echo "module_dir" | wc -l) != 1 ]]; then
            echo "Unrecognized add-on directory format. Skipping ${addon}."
            ERRORS+=("${addon}")
            return 0
        fi
        # Anki 2.0:
        zip -FS -r $exclude_string "${dist20_path}/${addon}-anki20.zip" *
        # Anki 2.1:
        cd "$module_dir"
        zip -FS -r $exclude_string "${dist21_path}/${addon}-anki21.zip" *
    fi

    cd "${wd_path}"

    return 0
}

# Main

if [[ "$ALL" == "false" && "$#" = "0" ]]; then
    echo "Error: no add-ons specified for '-f' option."
    exit 1
fi

if [[ ! -d "$src_path" ]]; then
    echo "Error: src directory not found. Exiting."
    exit 1
fi

# Compile exclude patterns
exclude_string=""
for pattern in "${excluded_patterns[@]}"; do
    exclude_string+="--exclude=${pattern} "
done
echo -e "Zip exclusion options: ${exclude_string}\n"

# Create build and dist directories
mkdir -p "${dist20_path}"
mkdir -p "${dist21_path}"

ERRORS=("")

if [[ "$ALL" == "true" ]]; then
    build_all
else
    build_specific "$@"
fi

echo -e "\nBuild complete."
if [[ -n "$ERRORS" ]]; then
    echo "Errors where encountered while processing the following add-ons: ${ERRORS[@]}"
fi
