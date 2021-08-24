FROM nvcr.io/nvidia/l4t-tensorflow:r32.6.1-tf2.5-py3
RUN apt-get update && apt-get install python3-dev git sudo unzip -y
RUN pip3 install -U pip
RUN pip3 install cffi setuptools pillow matplotlib notebook jetson-stats
WORKDIR /app/tf-trt
COPY *.sh ./
RUN sh install_protobuf-3.13.0.sh
RUN  cp -R /usr/local/lib/python3.6/dist-packages/protobuf-3.13.0-py3.6-linux-aarch64.egg/google/protobuf /usr/local/lib/python3.6/dist-packages/google/

COPY tf-trt.ipynb tf-trt.ipynb
COPY tf-trt-nano.ipynb tf-trt-nano.ipynb
RUN mkdir scripts
COPY scripts/* scripts/

# To Run : sudo docker run -it --rm --net=host --runtime nvidia  -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix nvcr.io/nvidia/l4t-base:r32.4.4

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]

