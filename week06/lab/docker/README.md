# TensorFlow with TensorRT (TF-TRT)

This is a very simple image classification example based on https://github.com/tensorflow/tensorrt/tree/master/tftrt/examples/image-classification updated to run on the Jetson Xavier NX.   You'll learn how to use TensorFlow 2.x to convert a Keras model to three tf-trt models, a fp32, fp16, and int8.  A simple set of test images will be used to both validate and benchmark both the native model and the three tf-trt ones.

## Jetpack Version
This should be done using JetPack 4.6.

## Running
This demo is made available as via a Dockerfile.  The image built from this demo leverages Nvidia's TensorFlow 2.x build (see https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html ) and requires an update to Protobuf.  There appears to be an issue with the python implementation protobuf (see https://jkjung-avt.github.io/tf-trt-revisited).  The current workaround is to build and install a C++ based implemenation. The script install_protobuf-3.13.0.sh will download, build, and install protobuf 3.13.0

Assuming you've checked out this repository on your Jetson, head to the subdirectory `quantization/tf-trt`.  From This directory, run the command `docker build -t tf-trt-demo .`.  This will take a bit of time to build.

Once the image is built, you can run the command `docker run -it --rm --net=host tf-trt-demo`.  Once the container is running, you'll see output similar to:
```
[I 21:26:42.668 NotebookApp] Writing notebook server cookie secret to /root/.local/share/jupyter/runtime/notebook_cookie_secret
[I 21:26:43.631 NotebookApp] Serving notebooks from local directory: /app/tf-trt
[I 21:26:43.631 NotebookApp] Jupyter Notebook 6.1.6 is running at:
[I 21:26:43.631 NotebookApp] http://nx:8888/?token=af4be11ce363992a3815f1893de5b4f219940a7fb364040a
[I 21:26:43.631 NotebookApp]  or http://127.0.0.1:8888/?token=af4be11ce363992a3815f1893de5b4f219940a7fb364040a
[I 21:26:43.631 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 21:26:43.647 NotebookApp] 
    
    To access the notebook, open this file in a browser:
        file:///root/.local/share/jupyter/runtime/nbserver-1-open.html
    Or copy and paste one of these URLs:
        http://nx:8888/?token=af4be11ce363992a3815f1893de5b4f219940a7fb364040a
     or http://127.0.0.1:8888/?token=af4be11ce363992a3815f1893de5b4f219940a7fb364040a
```
Navigate to the appropriate URL and open the file `tf-trt.ipynb`. 


Once the notebook is open, you may run each piece.  Note, the flush.sh script is available to clear cached memory if needed.  In addition, the notebook restarts a number of points to clear up memroy.

This image may be pulled (vs built) from the DockerHub registry `rdejana/tf-trt-demo`.



