# Lab 5 - Deep Learning Frameworks. Training image classifiers

This week we will practice writing basic training loops. If you have a Jetson NX, please use it; if not, the Nano is too underpowered for much of this, so please use Google Colab.

The Jetson NX device is far less powerful than the Cloud GPUs. But, it has 8G of accessible GPU memory and is quite modern (compatible with the instruction set present in Volta GPUs), so it's likely faster than your CPU laptop. Also, the code you write will be compatible; you could just run it "as is" on more powerful machines.

The Jetson Nano SoCs are based on the older, Maxwell, cores and don't have the Tensor cores. They also have less GPU memory - 2G or 4G.  This forces us to reduce batch sizes when training and use smaller models or risk OOM errors.

### 1a. Setup (Jetson NX)
Pull the latest ml container for the jetson from NGC and start it, passing through the GPU, port 8888, the drive where you keep your data. Make sure that the version you pull matches your Jetpack. For instance, if you have 32.6 installed:
```
docker pull nvcr.io/nvidia/l4t-ml:r32.6.1-py3
```
This default image contains TF2, PyTorch, Jupyter, as well a few common data science libraries. If you want to see how this image was build, look [here](https://github.com/dusty-nv/jetson-containers).

Start Jupyter Lab.  Note that the default password is `nvidia`

### 1b. Setup (Google Colab)
The easiest way to use Google Colab is to install the [Google Colab Chrome plugin](https://chrome.google.com/webstore/detail/open-in-colab/iogfkhleblhcpcekbiedikdehleodpjo?hl=en_). Once installed, you can navigate to the desired Jupyter notebook in Github, and then click the Extensions icon to the right of the URL location in the browser and select 'Open in Colab'

### 2a. Validate that a GPU is available (Jetson NX)
Please recall or look up the PyTorch and TensorFlow 2 commands that tell you whether you have at least one GPU available. It's a good idea to check because some repos will silently fall through to the CPU and run slowly. If your GPU was not correctly passed through, go back and re-run the container.

### 2b. Validate that a GPU is available (Google Colab)
Please recall or look up the PyTorch and TensorFlow 2 commands that tell you whether you have at least one GPU available. It's a good idea to check because some repos will silently fall through to the CPU and run slowly. If your GPU is not detected, click Runtime and Change Runtime type. How can you see the model of yor GPU?

### 3. Install Papermill (Jetson NX only)
Please review this section as it will be useful during the homework assignment.

[Papermill](https://papermill.readthedocs.io/en/latest/) comes in handy when you want to run your Jupyter notebooks programmatically, on the command line. This allows you to prototype locally and then submit your work with no changes to run on more powerful remote machines. Open up a terminal inside your Jupyter Lab and install papermill:
```
pip3 install papermill
```
### 4. Designate a parameters cell (Jetson NX only)
Please review this section as it will be useful during the homework assignment.

In your [lab template](https://github.com/MIDS-scaling-up/v3/blob/main/week05/lab/cifar_lab.ipynb) Jupyter notebook, tag one of the cells to be the parameter cell. At the moment, the ml image contains JupyterLab 2.2.9, so follow the instructions [here](https://papermill.readthedocs.io/en/latest/usage-parameterize.html#jupyterlab-2-0-2-2-x)

### 5. PyTorch - CIFAR10 classification
In this section, we will fill in the provided template and build an image classifier for the CIFAR10 dataset, which contains 60,000 32x32 color images that are sorted into 10 classes. Your goal is to quickly train a classifier from random weights -- and hey, you can do that on your NX!  You don't need to train all the way to the end, just run it for a few epochs to get a feel for how well it converges. Make sure that your _validation_ loss declines.  Make sure that you adjust the model architecture to the number of classes in CIFAR10 (10)!

### 6. PyTorch - CINIC10 dataset
The [CINIC](https://github.com/BayesWatch/cinic-10) dataset bridges us to the goal of our homework - training on ImageNet. These images are still 32x32, but you'll have to download this dataset separately -- we recommend pulling it from the [Kaggle Dataset](https://www.kaggle.com/mengcius/cinic10) because it's a lot faster. You'll need to uncompress it and then modify your code to use it instead of CIFAR10. Hint: use `datasets.ImageFolder`. Same as before, you don't need to run it forever, just run for a few epochs.

Google Colab notes:
* You will need your Google Drive account so that you can store the results of your work as well as some persistent files (such as creds)
* make sure you set up your [Kaggle API](https://www.kaggle.com/docs/api). 
* Download kaggle.json and store it in your Google Drive someplace (e.g. under MyDrive/.kaggle)
* When you run in your Colab notebook, copy this file to /root/.kaggle/kaggle.json and make sure the permissions on it are 600
* Now you should be able to use kaggle CLI commands (e.g. to download datasets). You can bake all these commands into your notebooks.

### 7. Run with papermill (Jetson NX only)
In this step, we will test that our notebook can be invoked programmatically, e.g.
```
papermill notebook.ipynb output.ipynb  -p param1 -p param2 ...
```
the `-p` directives will override the defaults provided in your jupyter cell

### 8. PyTorch Lightning
Now let's reformat this code for Pytorch Lightning! Fill in [this template](https://github.com/MIDS-scaling-up/v3/blob/main/week05/lab/cifar_lightning_lab.ipynb) with your code. 
