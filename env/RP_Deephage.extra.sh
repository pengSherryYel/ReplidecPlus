#!/usr/bin/bash

echo "downloading DeePhage"
git clone https://github.com/shufangwu/DeePhage.git ../resources/DeePhage
chmod -R 750 ../resources/DeePhage

echo "downloading MATLAB Runtime Installer need by DeePhage"
r_dir="../resources/mcr_tmp"
mcr94_dir='../resources/mcr_v94'
mcr94_dir_realpath=`realpath $mcr94_dir`
mkdir -p $r_dir
mkdir -p $mcr94_dir

cd $r_dir
wget https://ssd.mathworks.com/supportfiles/downloads/R2018a/deployment_files/R2018a/installers/glnxa64/MCR_R2018a_glnxa64_installer.zip 
unzip MCR_R2018a_glnxa64_installer.zip
./install -mode silent -agreeToLicense yes -destinationFolder $mcr94_dir_realpath
cd -
rm -rf $r_dir
