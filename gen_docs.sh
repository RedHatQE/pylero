#!/bin/bash
# Temporary until CI is setup to build documentation dynamically

# Use this script to generate documentataion locally, run './gen_docs.sh -h'
# from root of the directory for more info

# Backoff from any failure
set -euo pipefail

trap 'handle_error $? $LINENO' EXIT

handle_error(){
    if [ "$1" != "0" ]; then
        printf "Cleanup of any failures\n"
        printf "Error $1 occured on $2, cleaning docs if generated\n"
        [[ $(pwd) =~ doc$ ]] && make clean || rm -rf _build/*
        [[ $(pwd) =~ pylero$ ]] && make clean -C doc/ || rm -rf doc/_build/*
    fi
}

usage()
{
    echo
    echo "Generate documentation using Sphinx locally and remove 'username(-n)',"
    echo "'url(-u)', 'project(-p)' reference from docs"
    echo
    echo "Usage: ./gen_docs.sh [options]"
    echo "options:"
    echo "  n   Name of the Polarion user."
    echo "  u   URL of Polarion local instance."
    echo "  p   Project of Polarion local instance."
    echo "  h   Print this help."
    echo
}

if [[ $# -eq 0 ]] ; then
    usage 1>&2
    exit -1
fi

# Install sphinx if not installed
if ! command -v sphinx-build 1>/dev/null; then
    echo "'sphinx-build' is required but not found in PATH, do you wish to install (Sphinx v3.4.3) via Pip?"
    select yn in "Yes" "No"; do
        case $yn in
            Yes ) pip install sphinx==3.4.3; break;;
            No ) echo "Can't procced without sphinx-build"; exit -1;;
        esac
    done
fi

options=":n:u:p:h"
name=""
url=""
project=""

while getopts $options opt; do
   case ${opt} in
    n )
        name=$OPTARG
        ;;
    u )
        url=$OPTARG
        ;;
    p )
        project=$OPTARG
        ;;
    h )
        usage
        exit;;
    \? )
        printf "\nInvalid Option: -$OPTARG\n" 1>&2
        usage 1>&2
        exit;;
    : )
        printf "\nInvalid option: $OPTARG requires an argument\n" 1>&2
        usage 1>&2
        exit;;
   esac
done

shift $((OPTIND -1))
if [ -z "$name" ] || [ -z "$url" ] || [ -z "$project" ]; then
    printf "\nMissing -n or -u or -p\n" 1>&2
    usage 1>&2
    exit -1
fi

# Copy Pylero configuration file to doc directory
[ -e $HOME/.pylero ] && cp $HOME/.pylero .pylero
[ -e .pylero ] && cp .pylero doc/.pylero

# Generate documentaion
cd doc/
make clean
make html
cd - 1>/dev/null

# Replace all internal references
build_dir="doc/_build/html"
rm -rf doc/_build/doctrees
echo
echo Reference of "'$name'" will be changed to 'POLARION_USERNAME' in below files
grep -riln $name $build_dir | tee /dev/tty | xargs sed -i "s|$name|POLARION_USERNAME|gi"

echo
echo Reference of "'$url'" will be changed to 'POLARION_URL' in below files
grep -riln $url $build_dir | tee /dev/tty | xargs sed -i "s|$url|POLARION_URL|gi"

echo
echo Reference of "'$project'" will be changed to 'POLARION_PROJECT' in below files
grep -riln $project $build_dir | tee /dev/tty | xargs  sed -i "s|$project|POLARION_PROJECT|gi"

echo

# Need to have 'docs' folder for serving from github pages
rm -rf docs
$(shopt -s dotglob; mv -f $build_dir docs)
ln -fsvr docs "doc/_build/"
touch docs/.nojekyll
echo "Done! Docs can be served from 'docs' folder"
