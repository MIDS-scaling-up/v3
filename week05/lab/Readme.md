# Lab 5 - Deep Learning Frameworks. Training image classifiers

This week we will practice writing basic training loops. We will use our Jetson NX device for quick prototyping. Of course, it's far less powerful than the Cloud GPUs. But, it's little GPU is quite modern (compatible with the instruction set present in Volta GPUs), so it's likely faster than your CPU laptop. Also, the code you write will be compatible; you could just run it "as is" on more powerful machines.

### 1. Setup
Pull the latest ml container for the jetson from NGC and start it, passing through the GPU, port 8888, the drive where you keep your data. Make sure that the version you pull matches your Jetpack. For instance, if you have 32.5 installed:
```
docker pull nvcr.io/nvidia/l4t-ml:r32.5.0-py3
```
This default image contains TF2, PyTorch, Jupyter, as well a few common data science libraries. If you want to see how this image was build, look [here](https://github.com/dusty-nv/jetson-containers).

Start Jupyter Lab.  Note that the default password is `nvidia`

### 2. Validate that a GPU is available
Please recall or look up the PyTorch and TensorFlow 2 commands that tell you whether you have at least one GPU available. It's a good idea to check because some repos will silently fall through to the CPU and run slowly. If your GPU was not correctly passed through, go back and re-run the container.

### 3. Install Papermill
[Papermill](https://papermill.readthedocs.io/en/latest/) comes in handy when you want to run your Jupyter notebooks programmatically, on the command line. This allows you to prototype locally and then submit your work with no changes to run on more powerful remote machines. Open up a terminal inside your Jupyter Lab and install papermill:
```
pip3 install papermill
```
### 4. Designate a parameters cell
In your (new) Jupyter notebook, tag one of the cells to be the parameter cell. At the moment, the ml image contains JupyterLab 2.2.9, so follow the instructions [here]https://papermill.readthedocs.io/en/latest/usage-parameterize.html#jupyterlab-2-0-2-2-x)

### 5. PyTorch - CIFAR10 classification
In this section, we will use the provided template and build an image classifier for the CIFAR10 dataset, which contains 60,000 32x32 color images that are sorted into 10 classes. Your goal is to quickly train a classifier from random weights -- and hey, you can do that on your NX!  You don't need to train all the way to the end, just run it for a few epochs to get a feel for how well it converges. Make sure that your _validation_ loss declines.

### 6. PyTorch - CINIC10 dataset
The [CINIC](https://github.com/BayesWatch/cinic-10) dataset bridges us to the goal of our homework - training on ImageNet. These images are still 32x32, but you'll have to download this dataset separately -- we recommend pulling it from the [Kaggle Dataset](https://www.kaggle.com/mengcius/cinic10) because it's a lot faster. You'll need to uncompress it and then modify your code to use it instead of CIFAR10. Hint: use `datasets.ImageFolder`. Same as before, you don't need to run it forever, just run for a few epochs.

### 7. Run with papermill
In this step, we will test that our notebook can be invoked programmatically, e.g.
```
papermill notebook.ipynb output.ipynb  -p param1 -p param2 ...
```
the `-p` directives will override the defaults provided in your jupyter cell

### 8. PyTorch Lightning
Now let's reformat this code for Pytorch Lightning!
