#!/usr/bin/bash

git clone https://github.com/KennthShang/PhaBOX.git ../resources/PhaBOX

cd ../resources/PhaBOX

# database
echo "Downloading database"
if [ ! -e "phabox_db_v2.zip" ];then
wget https://github.com/KennthShang/PhaBOX/releases/download/v2/phabox_db_v2.zip
unzip phabox_db_v2.zip
else
echo "file exist! skip"
fi

