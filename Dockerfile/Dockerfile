# docker build -t ubuntu1604py36
FROM ubuntu:16.04

RUN apt-get update 
RUN apt-get install -y software-properties-common vim build-essential google-perftools libbz2-dev libxml2-dev libjemalloc-dev openssl libcurl4-openssl-dev libssl-dev libtbb-dev libarmadillo-dev libgsl-dev

RUN apt-get install -y wget
#install cmake
RUN mkdir -p /tmp/cmake_build && cd /tmp/cmake_build && wget https://cmake.org/files/v3.12/cmake-3.12.4.tar.gz && tar xf cmake*.tar.gz && cd cmake* && ./bootstrap && make && make install && rm -fr /tmp/cmake_build
