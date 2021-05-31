# Homework 5 - Deep Learning Frameworks - Training an image classifier on the ImageNet dataset from random weights.

This is a graded homework.  IT IS CURRENTLY UNDER DEVELOPMENT AND WILL BE FINALIZED SHORTLY

Due just before week 6 session

### The goal
The goal of the homework is to train an image classification network on the ImageNet dataset to the Top 1 accuracy of 65% or higher.

We suggest that you use PyTorch or PyTorch Lightning.  

The lab 6 materials ought to help you prepare for the homework.

### The steps
The steps are roughly as follows:

1. Procure a virtual machine in AWS - we recommend a T4 GPU and 1 TB of space (e.g. g4dn.2xlarge). Use the Nvidia Deep Learning AMI so that the pre-requisites are pre-installed for you. We recommend using the latest [nvidia pytorch container](https://ngc.nvidia.com/catalog/containers/nvidia:pytorch)
2. Download the ImageNet dataset to your VM. Please do register at [image-net.org](https://image-net.org/) for all of your future needs. Given the slowness of download via this web site, however, we have downloaded a copy of ImageNet for you and will distribute it in class.
3. Prepare the dataset:
  * create train and val subdirectories and move the train and val tar files to their respective locations
  * untar both files and remove them as you no longer neeed them
  * Use the following [shell script](https://raw.githubusercontent.com/soumith/imagenetloader.torch/master/valprep.sh) to process your val directory. It simply moves your validation set into proper subfolders
  * When you untarred the train file, it created a large number (1000) of tar files, one for each class.  You will need to create a separate directory for each of class , move the tar file there, untar the file and remove it. This should be a one liner shell script but we'll let you have fun with it!
  * Make sure that under the train and val folders, there is one directory for class and that the samples for that class are under that directory
5. Adapt the code we discuss in the labs to the training of imagenet
6. Start training && observe progress !


### The decisions
Which architecture to choose? Another, hopefully a much easier one, when to stop training? We conscuously set the bar at 65% Top1 (on the validation set) so that you may not need to choose a very heavy model and / or train it forever.

### Extra credit
Create your own model architecture. You can draw your inspiration from the [PyTorch Resnet github](https://github.com/pytorch/vision/blob/master/torchvision/models/resnet.py), for instance.


### To turn in
Please turn in your training logs. They should obviously display that you have achieved the Top 1 accuracy.  Also, please save / download the trained weights to your jetson device for evaluation later.
