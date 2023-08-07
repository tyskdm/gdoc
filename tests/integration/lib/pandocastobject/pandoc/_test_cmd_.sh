#! /bin/sh

if [ $# -ne 1 ]; then
    echo "EXIT(1): NO_OPT" 1>&2
    return 1
elif [ "$1" = "--version" ]; then
    echo "pandoc 2.14.2"
    echo "Compiled with pandoc-types 1.22.2.1, Commandline opt = $1"
    return 0
else
    echo "Exit(0): WITH_OPT"
    echo "OPT = $1"
    return 0
fi
