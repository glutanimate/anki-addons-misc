#!/bin/bash
# Builds zip files for Anki 2.1

set -ue

# Global variables
source_dir="./src"
build_dir="./build"
excluded_patterns=("__pycache__" "meta.json" "*.pyc" "*.pyo" "*.html" "*.md")

# Compile exclude patterns
exclude_string=""
for pattern in "${excluded_patterns[@]}"; do
    exclude_string+="--exclude=${pattern} "
done

echo "Building anki-addons-misc..."
echo "Exclusion options: ${exclude_string}"

mkdir -p "${build_dir}"

# Iterate over stc directories and build zip files
while IFS= read -d $'\0' -r addon_dir ; do
    base=$(basename "${addon_dir}")
    echo "Building ${base}.zip..."
    zip -FS -j -r $exclude_string "${build_dir}/${base}.zip" "${addon_dir}"/*
done < <(find "$source_dir" -mindepth 1 -maxdepth 1 -type d -print0)