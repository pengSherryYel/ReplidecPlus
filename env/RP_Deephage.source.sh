#!/usr/bin/env bash

declare -r SCRIPT_NAME=$(readlink -f ${BASH_SOURCE[0]})

script_realpath=`realpath -s $SCRIPT_NAME`
script_dirname=`dirname $script_realpath`
mcr94_dir="$script_dirname/../resources/mcr_v94"
mcr94_dir_realpath=`realpath $mcr94_dir`

export LD_LIBRARY_PATH=$mcr94_dir_realpath/v94/runtime/glnxa64:$mcr94_dir_realpath/v94/bin/glnxa64:$mcr94_dir_realpath/v94/sys/os/glnxa64:$mcr94_dir_realpath/v94/extern/bin/glnxa64:$LD_LIBRARY_PATH
