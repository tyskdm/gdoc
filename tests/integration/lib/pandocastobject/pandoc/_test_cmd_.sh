#! /bin/sh

if [ $# -ne 1 ]; then
    echo "EXIT(1): NO_OPT" 1>&2
    echo "Try --help for more infomation." 1>&2
    return 1
else
    echo "_test_cmd_ 2.14.2"
    echo "Commandline opt = $1"
    return 0
fi
