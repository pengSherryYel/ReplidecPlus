#!/usr/bin/bash

mkdir resources
cd env
echo "prepare base env"
conda env create -n RP_base --file ./RP_base.yml

echo "prepare phact"
conda env create -n RP_phacts --file ./RP_phacts.yml

echo "prepare bacphlip"
conda env create -n RP_bacphlip --file ./RP_bacphlip.yml

echo "prepare deephage"
conda env create -n RP_deephage --file RP_Deephage.yml
sh RP_Deephage.extra.sh

echo "prepare phabox"
conda env create -n RP_phabox --file RP_phabox.yml
sh RP_phabox.extra.sh

echo 'prepare replidec'
conda create -n RP_replidec -c bioconda replidec

echo 'prepare phageAI'
conda env create -n RP_phageai --file RP_phageai.yml

echo 'YEAH!! Enviroment prepare done!!'


