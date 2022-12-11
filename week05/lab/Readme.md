# Lab 5 - Deep Learning Frameworks. Training image classifiers

This week we will practice writing basic training loops. We need GPUs for this and will use Google Colab. To enable GPU in your notebook, select the following menu options − "Runtime -> Change runtime type". In the dropdown of "None/GPU/CPU", select "GPU" so that your notebook can use free GPU during processing. 
 
### 1. Setup  
The easiest way to use Google Colab is to install the [Google Colab Chrome plugin](https://chrome.google.com/webstore/detail/open-in-colab/iogfkhleblhcpcekbiedikdehleodpjo?hl=en_). Once installed, you can navigate to the desired Jupyter notebook in Github, and then click the Extensions icon to the right of the URL location in the browser and select 'Open in Colab'
 
### 2. Validate that a GPU is available  
Please recall or look up the PyTorch and TensorFlow 2 commands that tell you whether you have at least one GPU available. It's a good idea to check because some repos will silently fall through to the CPU and run slowly. If your GPU is not detected, click Runtime and Change Runtime type. How can you see the model of yor GPU?
 
### 3. PyTorch - CIFAR10 classification
In this section, we will fill in the provided template and build an image classifier for the CIFAR10 dataset, which contains 60,000 32x32 color images that are sorted into 10 classes. Your goal is to quickly train a classifier from random weights -- and hey, you can do that on your NX!  You don't need to train all the way to the end, just run it for a few epochs to get a feel for how well it converges. Make sure that your _validation_ loss declines.  Make sure that you adjust the model architecture to the number of classes in CIFAR10 (10)!

### 4. PyTorch - CINIC10 dataset
The [CINIC](https://github.com/BayesWatch/cinic-10) dataset bridges us to the goal of our homework - training on ImageNet. These images are still 32x32, but you'll have to download this dataset separately -- we recommend pulling it from the [Kaggle Dataset](https://www.kaggle.com/mengcius/cinic10) because it's a lot faster. You'll need to uncompress it and then modify your code to use it instead of CIFAR10. Hint: use `datasets.ImageFolder`. Same as before, you don't need to run it forever, just run for a few epochs.

Google Colab notes:
* You will need your Google Drive account so that you can store the results of your work as well as some persistent files (such as creds)
* make sure you set up your [Kaggle API](https://www.kaggle.com/docs/api). 
* Download kaggle.json and store it in your Google Drive someplace (e.g. under MyDrive/.kaggle)
* When you run in your Colab notebook, copy this file to /root/.kaggle/kaggle.json and make sure the permissions on it are 600
* Now you should be able to use kaggle CLI commands (e.g. to download datasets). You can bake all these commands into your notebooks.

### 5. PyTorch Lightning
Now let's reformat this code for Pytorch Lightning! Fill in [this template](https://github.com/MIDS-scaling-up/v3/blob/main/week05/lab/cifar_lightning_lab.ipynb) with your code. 
