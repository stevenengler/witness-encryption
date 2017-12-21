FROM ubuntu:16.04

WORKDIR /app

ADD . /app/witness-encryption

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt install -y wget bzip2 git autoconf libtool apt-utils build-essential swig

RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -p /app/miniconda3
ENV PATH="/app/miniconda3/bin:${PATH}"

RUN conda update conda && conda install anaconda && pip install unitconvert

RUN apt install -y libgmp10 libgmp3-dev libgmpxx4ldbl libgmp-dev
RUN apt install -y libmpfr4 libmpfr4-dbg libmpfr-dev libmpfr-doc

RUN git clone https://github.com/stevenengler/new-multilinear-maps.git
RUN git clone https://github.com/fplll/fplll.git && cd fplll && git checkout 7d76d7400744

ENV LD_LIBRARY_PATH="/usr/local/lib/:${LD_LIBRARY_PATH}"

RUN cd fplll && ./autogen.sh && ./configure && make && make check && make install
RUN cd new-multilinear-maps && python setup.py install
