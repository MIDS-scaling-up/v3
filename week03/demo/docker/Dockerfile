# Using ubuntu 18.04 as base image
FROM ubuntu:18.04
# update the base image
RUN apt-get update && apt-get -y update
# install 
RUN apt-get install python3-pip python3-dev build-essential nodejs -y
# make python3 -> python
RUN ln -s /usr/bin/python3 /usr/local/bin/python 
# update pip
RUN pip3 install --upgrade pip
# install jupyter and lab
RUN pip3 install jupyter
RUN pip3 install jupyterlab
# set our workdir
WORKDIR /src/notebooks
# Copy our notebook over
COPY notebooks/simple.ipynb ./
# Setup which command to run...
# This runs jup notebook 
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
# This runs jup lab
#CMD ["jupyter", "lab", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
