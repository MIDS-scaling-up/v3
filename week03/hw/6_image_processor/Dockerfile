FROM ubuntu 

RUN apt-get update
RUN apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl vim-tiny \
    gnupg-agent \
    software-properties-common

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3.6 \
    python3-pip \
    python3-opencv \
    vim \
    libhdf5-dev \
    python3-setuptools \
    python3-h5py \
    python3-wheel

RUN apt-get clean

RUN apt install -y mosquitto-clients
RUN pip3 install paho-mqtt

# example from https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
COPY imageprocessor.py imageprocessor.py
CMD ["python3", "imageprocessor.py"]
