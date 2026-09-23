#!/usr/bin/bash
set -euxo pipefail

mkdir resources
cd env
echo "prepare base env"
conda env create -n RP_base --file ./RP_base.yml
conda clean -afy

#echo "prepare phact"
#conda env create -n RP_phacts --file ./RP_phacts.yml

echo "prepare bacphlip"
conda env create -n RP_bacphlip --file ./RP_bacphlip.yml
conda clean -afy

echo "prepare deephage"
conda env create -n RP_deephage --file RP_Deephage.yml
sh RP_Deephage.extra.sh
conda clean -afy

echo "prepare phabox"
conda create -n RP_phabox phabox=2.1.13 -c conda-forge -c bioconda -y
sh RP_phabox.extra.sh
conda clean -afy

echo 'prepare replidec'
conda create -n RP_replidec -c bioconda -c conda-forge replidec=0.3.6 -y
conda clean -afy

#echo 'prepare phageAI'
#conda env create -n RP_phageai --file RP_phageai.yml

echo 'YEAH!! Enviroment prepare done!!'


