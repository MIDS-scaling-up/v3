# Homework 9 - Distributed training

This is a graded homework

Due: before week 10 begins

In this homework, we are focused on aspects of multi-node and multi-gpu (mnmg) model training.
The high level idea is to practice running multi-node training by adapting the code we develop in homework 5 (imagenet training from random weights) to run on two nodes instead of one.

Notes:
* You will need to provision two g4dn.2xlarge instances. Each has 8 vCPUs, so you'll need to the ability (limit) to provision 16 vCPUs. 
* You'll need to provision a 300 GB EFS volume and mount it on both instances
* You'll need to [re-] download imagenet2012 (we'll provide links in class again) and unpack it 
* You'll need to demonstrate your command of [PyTorch DDP](https://pytorch.org/tutorials/beginner/dist_overview.html)
* Apply [PyTorch native AMP](https://pytorch.org/docs/stable/amp.html)
* Document your run using [Tensorboard](https://www.tensorflow.org/tensorboard) or [Weights and Biases](https://wandb.ai/home) 
* Hopefully, demonstrate that your training is 2x faster than on a single GPU

Tips:
coming shortly


