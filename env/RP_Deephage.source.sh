#!/usr/bin/bash

mcr94_dir='../resoruces/mcr_v94'
mcr94_dir_realpath=`realpath $mcr94_dir`

export LD_LIBRARY_PATH=$mcr94_dir_realpath/v94/runtime/glnxa64:$mcr94_dir_realpath/v94/bin/glnxa64:$mcr94_dir_realpath/v94/sys/os/glnxa64:$mcr94_dir_realpath/v94/extern/bin/glnxa64:$LD_LIBRARY_PATH
