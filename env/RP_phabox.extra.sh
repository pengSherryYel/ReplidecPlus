#!/usr/bin/bash

#git clone git@github.com:KennthShang/PhaBOX.git ../resources/PhaBOX

cd ../resources/PhaBOX

# database
echo "Downloading database"
if [ ! -e "phagesuite_database.zip" ];then
fileid="1hjACPsIOqqcS5emGaduYvYrCzrIpt2_9"
filename="phagesuite_database.zip"
html=`curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}"`
curl -Lb ./cookie "https://drive.google.com/uc?export=download&`echo ${html}|grep -Po '(confirm=[a-zA-Z0-9\-_]+)'`&id=${fileid}" -o ${filename}
else
echo "file exist! skip"
fi

# initial files
if [ ! -e "phagesuite_parameters.zip" ];then
fileid="1E94ii3Q0O8ZBm7UsyDT_n06YekNtfV20"
filename="phagesuite_parameters.zip"
html=`curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}"`
curl -Lb ./cookie "https://drive.google.com/uc?export=download&`echo ${html}|grep -Po '(confirm=[a-zA-Z0-9\-_]+)'`&id=${fileid}" -o ${filename}
else
echo "file exist! skip"
fi

unzip phagesuite_database.zip
unzip phagesuite_parameters.zip

conda_path=`which conda`
conda_tmp=`dirname $conda_path`
conda_home=`dirname $conda_tmp`
cp blastxml_to_tabular.py  $conda_home/envs/RP_phabox/bin/blastxml_to_tabular.py
chmod 777 $conda_home/envs/RP_phabox/bin/blastxml_to_tabular.py
rm -rf phagesuite_database.zip phagesuite_parameters.zip
cd -
