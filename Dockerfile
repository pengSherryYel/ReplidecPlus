FROM ubuntu:latest

## use bash instead of sh
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

## useful tools
RUN apt-get update && apt-get install -y \
    software-properties-common \
    python3-pip \
    git \
    wget \
    curl \
    unzip \
    libxt6 \
    && rm -rf /var/lib/apt/lists/*

# ----------- install Miniconda -----------
# 1. install Miniconda
ENV CONDA_DIR /opt/conda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh

# 2. install Conda to /opt/conda
RUN bash miniconda.sh -b -p $CONDA_DIR \
&& rm miniconda.sh

# 3. add Conda to PATH env
ENV PATH="$CONDA_DIR/bin:$PATH"
#RUN conda init bash

# ----------- install  ReplidecPlus ---------
## output dir
RUN mkdir -p /data && \
    chmod 755 /data

## workdir
WORKDIR /usr/src/replidecplus
ENV RP_DIR /usr/src/replidecplus

## download from git
RUN cd $RP_DIR
RUN git clone https://github.com/pengSherryYel/ReplidecPlus.git 
RUN cd $RP_DIR/ReplidecPlus && bash prepare_env.sh
RUN export PATH=/usr/src/replidecplus/ReplidecPlus:$PATH

## download database of Replidec
RUN cd $(find /opt/conda/envs/RP_replidec/lib -path '*/site-packages/Replidec' -type d) && \
wget https://zenodo.org/records/15781219/files/db_v0.3.2.tar.gz && \
tar -zxvf db_v0.3.2.tar.gz

## activate conda
#SHELL ["/bin/bash", "-c"]
RUN echo ". /opt/conda/etc/profile.d/conda.sh" >> /root/.bashrc 
#echo "conda activate RP_base" >> ~/.bashrc && . /root/.bashrc
#ENTRYPOINT ["""python"]
