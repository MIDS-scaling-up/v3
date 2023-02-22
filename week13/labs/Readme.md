## Week 13 labs - everything accelerated!

### Triton Inference Server primer
Triton Inference server is designed to help you create services out of your trained models.  In this lab, we will follow the [Triton IS QuickStart](https://github.com/triton-inference-server/server/blob/main/docs/quickstart.md). A few quick notes:
* First, provision a g4dn.2xlarge virtual machine in AWS. Use the Nvidia Deep Learning AMI.
* Go to your home diretory and clone the Triton IS server repo, e.g. ```https://github.com/triton-inference-server/server.git```
* The current tag is 22.06, so the pull commands are:
```
docker pull nvcr.io/nvidia/tritonserver:22.06-py3-sdk (client)
docker pull nvcr.io/nvidia/tritonserver:22.06-py3 (server)
```
A few quick questions:
* is your server using the GPU?
* Can you change the number of classes for scoring in the example?
* Which model is being used for inference? Can you change it to a different model?
* Can you get the metrics for your server?

### RAPIDS primer
RAPIDS is an open source project that targets to bring GPU acceleration to typical data science tasks.  Please refer to the async materials for more information on the project or visit [The RAPIDS homepage](https://rapids.ai/)
For this lab, we'll be using the latest rapids container. From your home directory in your VM, pull and start the rapids container.
```
docker run -p 8888:8888 --gpus=all -ti nvcr.io/nvidia/rapidsai/rapidsai:22.06-cuda11.5-base-ubuntu20.04-py3.9
# the latest rapids container no longer has jupyter lab, sigh
conda install -y -c conda-forge jupyterlab
# start jupyter lab
jupyter-lab --allow-root --ip=0.0.0.0 --no-browser
```
Try the following notebooks:
* Download the [Colab example](https://colab.research.google.com/drive/1rY7Ln6rEE1pOlfSHCYOVaqt8OvDO35J0#forceEdit=true&offline=true&sandboxMode=true) and run it in your Jupyter notebook.  Skip the cells that deal with RAPIDS installation. Note how easy it is to use CuDF and CuML
* Open up a terminal and clone the examples repo: `git clone https://github.com/rapidsai/notebooks.git`
* go to the notebooks directory and pull the submodules: `sh update.sh`
* Under the cuml folder, run through the K-means demo example. What is the speedup you get?
* Under the same folder, run through the random forest example.  What is the speedup you get?
* Under the xgboost folder, run the XGBoost demo. Repeat on the CPU. What is the speedup?

### DALI primer
DALI stands for Data Loading Library.  This Open Source project is another tool in our arsenal to eliminate or at least reduce CPU bottlenecks in our pipelines.  We did not cover DALI in the async material since it was very new, but now it's part of most Nvidia accelerated pipelines and is present in all Deep Learning NGC containers.

* Please glance through the [DALI Documentation](https://docs.nvidia.com/deeplearning/dali/user-guide/docs/index.html)
* Start the pytorch ngc container, e.g. ```docker run --rm --gpus all -p 8888:8888 --ipc=host -ti  nvcr.io/nvidia/pytorch:22.06-py3``` and then start jupyter lab , e.g. ```jupyter lab --ip=0.0.0.0 --allow-root```
* Upload the [Getting Started](getting_started_dali.ipynb) example to your jupyter environment and run through it. What acceleration did you get in the last cell? Can you suggest what contributes to that number?

### GFP-GAN 
GFP-GAN stands for "Generative Facial Prior Generative Adversarial Network". It is used for blind face restoration. GFP is incorporated into the face restoration process via channel-split spatial feature transform layers, which allow for a good balance between realness and fidelity. The goal of this lab is to experiment with the model(s) and evaluate the GAN performance against a baseline of your own photo, taken with the camera on your device and artificially converted into a retro image. 

Try the following:
* minimal setup: deploy and run CPU-based model on your desktop or laptop, levaraging the provided [Jupyter notebook](https://github.com/alsavelv/v3/blob/main/week13/labs/GFPGAN_demo_w251.ipynb) for generating a photo collage
* more advanced: do the same on your Jetson 
* extra bonus: deploy and run GPU-based model with colorization (either on Jetson or on your device, if it has GPU)

Detailed instructions for model installation and scripts for running inferences are provided both in [the repo](https://github.com/TencentARC/GFPGAN). Please copy the Jupyter notebook to the root of the cloned repo and run it from there, as it executes some commands that depend on this code. The notebook was created for a Windows-based setup. Minor changes to scripts will be required to make it compatible with Mac and Linux. Also, make sure to update directory paths to match your setup.

Once you get the inference result, you can experiment with different types of filters, increasing or decreasing the level of photo distortion, image resolution, using colored or monochrome images, etc. Once you get sufficient impression, think critically about the quality of the output produced by the model. Keep in mind that the photo impression is created by a combination of many factors, including facial features, emotions, colors, etc. Imagine, for the sake of an argument, that in a few hundred years the "vintage" version of the photo is the only digital trace that left of you for your ancestors; would you be comfortable to let them rely on the result of processing it with GFP-GAN, or prefer to use the low-quality image as is? This perspective is important, because people whose images were taken in late 19th/20th century are in this position, having their old photographs restored with AI. Think about possible impacts of inaccurate photo restoration in other scenarios. Also, consider whether overreliance on AI in general and for photo restoration specifically can be mitigated, and in which ways.
