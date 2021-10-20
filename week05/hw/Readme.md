# Homework 5 - Deep Learning Frameworks - Training an image classifier on the ImageNet 2012 dataset from random weights.

This is a graded homework.

Due just before week 5 session

### The goal
The goal of the homework is to train an image classification network on the ImageNet dataset to the Top 1 accuracy of 60% or higher.

We suggest that you use PyTorch or PyTorch Lightning.  

The lab 6 materials ought to help you prepare for the homework.

### The steps
The steps are roughly as follows:

1. Procure a virtual machine in AWS - we recommend a T4 GPU and 1 TB of space (e.g. g4dn.2xlarge). Use the Nvidia Deep Learning AMI so that the pre-requisites are pre-installed for you. We recommend using the latest [nvidia pytorch container](https://ngc.nvidia.com/catalog/containers/nvidia:pytorch)
2. Download the ImageNet dataset to your VM. Please do register at [image-net.org](https://image-net.org/challenges/LSVRC/2012/index.php) for all of your future needs. Given the slowness of download via this web site, however, we have downloaded a copy of ImageNet for you and will distribute it in class. (FYI - some students found [this link](https://github.com/facebookarchive/fb.resnet.torch/blob/master/INSTALL.md#download-the-imagenet-dataset) helpful for downloading)
3. Prepare the dataset:
  * create train and val subdirectories and move the train and val tar files to their respective locations
  * untar both files and remove them as you no longer neeed them
  * Use the following [shell script](https://raw.githubusercontent.com/soumith/imagenetloader.torch/master/valprep.sh) to process your val directory. It simply moves your validation set into proper subfolders
  * When you untarred the train file, it created a large number (1000) of tar files, one for each class.  You will need to create a separate directory for each of class , move the tar file there, untar the file and remove it. This should be a one liner shell script but we'll let you have fun with it!
  * Make sure that under the train and val folders, there is one directory for class and that the samples for that class are under that directory
5. Adapt the code we discuss in the labs to the training of imagenet. Make sure the number of classes and image sizes are correct. Make sure the transforms are correct.
6. Start training && observe progress !


### Key decisions to consider
* Which architecture to choose? Here's what [Torchvision has](https://pytorch.org/vision/stable/models.html) but obviously you're not limited to that if you want to try something newer.
* Which optimizer to use? For this homework we recommend [SGD](https://pytorch.org/vision/stable/models.html) for simplicity.
* What should the learning rate be? This is where we need to check our sources / see how others trained the model.
* Should we change the learning rate while training? Our suggestion would be to use something simple: e.g. drop it 10x every 33% of training time.
* When to stop training? We conscuously set the bar at 60% Top1 (on the validation set) so that you may not need to choose a very heavy model and / or train it forever.

### Please note
* Please do not attempt to spend more than 3 days training your model on a single T4 GPU. If your estimate gives you a longer training time, pick a different approach.
* You might want to prototype your work using Jupyter and then submit it using [papermill](https://papermill.readthedocs.io/en/latest/usage-cli.html)

### Extra credit
Create your own model architecture. You can draw your inspiration from the [PyTorch Resnet github](https://github.com/pytorch/vision/blob/master/torchvision/models/resnet.py), for instance.


### To turn in
Please turn in your training logs. They should obviously display that you have achieved the Top 1 accuracy.  Also, please save / download the trained weights to your jetson device for evaluation later.
