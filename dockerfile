FROM ubuntu:bionic

RUN apt-get update

RUN DEBIAN_FRONTEND=noninteractive apt-get -y install git\
        python3 \
        python3-pip \
        libzmq3-dev \
        libusb-1.0-0-dev

RUN pip3 install Jetson.GPIO pyftdi zmq



