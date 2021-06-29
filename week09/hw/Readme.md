# Homework 9 - Distributed training

This is a graded homework

Due: before week 10 begins

In this homework, we are focused on aspects of multi-node and multi-gpu (mnmg) model training.
The high level idea is to practice running multi-node training by adapting the code we develop in homework 5 (imagenet training from random weights) to run on two GPU nodes instead of one.

Notes:
* You will need to provision two g4dn.2xlarge instances. Each has 8 vCPUs, so you'll need to the ability (limit) to provision 16 vCPUs. 
* We recommend adding 400GB of storage space under /root so that you can comfortably work with imagenet2012 (below)
* You'll need to [re-] download imagenet2012 (we'll provide links in class again) and unpack it on each machine -- e.g. under /data/
* You'll need to demonstrate your command of [PyTorch DDP](https://pytorch.org/tutorials/beginner/dist_overview.html)
* Apply [PyTorch native AMP](https://pytorch.org/docs/stable/amp.html)
* Document your run using [Tensorboard](https://www.tensorflow.org/tensorboard) or [Weights and Biases](https://wandb.ai/home) 
* Hopefully, demonstrate that your training is ~2x faster than on a single GPU machine.

Tips:
* You could trt using g4dn.xlarge, but in our experience, they just don't have enough CPUs to keep the GPU fed, so the results will be slow.
* Ideally, you should be able to use EFS.  However, one must ensure that performance is good-- and we've seen issues.
* There is no need to train to the end (e.g. 90 epochs); it would be sufficient to run the training for 1-2 epochs, time it, and compare the results against a run on a sinle GPU instance.
* Please monitor the GPU utilization using nvidia-smi; as long as both GPUs are > 95% utilized, you are doing fine.


