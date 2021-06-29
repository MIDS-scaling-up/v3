# Lab 9 - Distributed training



These labs will be focused on aspects of multi-gpu and multi-node model training.
The exercises would involve training networks (NLP, CV) with a focus on data parallelism.

For labs 1-3, you will need to provision a single g4dn.2xlarge instance with ~100 GB of disk space in / . Please choose the Nvidia Deep Learning image.  As before , and for simplicity, you will need to open up all TCP ports (0-65535) for communication in the associated security group[s].

You will need to download the CINIC dataset. The instructors will distribute a link to the s3 bucket.

Lab 4 will be done in teams using instructor-provided VMs. For lab 5, you will need a pair of VMs. That lab could be done in groups or individually. You will need the ability to provision 16 vCPUs (two VMs, 8 cVPUs each).

### Lab 1. Automatic Mixed Precision (AMP)
In this lab, we will start with a previously discussed [CINIC example](cinic.ipynb). You will need to add the [Torch AMP](https://pytorch.org/docs/stable/amp.html) to the code.  Please change the code to set the GPU number (0), increase the batch size to fill the GPU, and use a heavier network (resnet152). Does AMP improve performance? Does it allow you to increase batch size while training?

### Lab 2. Using Tensorboard to monitor experiments
Read through [TORCH.UTILS.TENSORBOARD docs](https://pytorch.org/docs/stable/tensorboard.html). Use SummaryWriter() to log acc1, acc5, loss, and learning rate. Hint: you'll need to do something like `writer.add_scalar("Loss/train", loss, global_step = global_step)`, keeping track of your global step for a nice graph.

Launch tensorboard, eg.
```
# the logdir should match the parameter passed to what you pass to SummaryWriter, e.g.
# writer = SummaryWriter(log_dir="/data/runs/")
tensorboard --logdir=/data/runs
```
Then you should be able to connect to the ip address of your VM on port 6006

### Lab 3. Using Weights and Biases (Wandb) to monitor experiments
Similar to the previous section, instead of SummaryWriter, peruse the [Wandb Quickstart](https://docs.wandb.ai/quickstart) and `wandb.log` to log the parameters during the experiment. You should be able to log into Wandb and see your stats updated in real time.

### Lab 4. Using Data Parallelism (DP) to run the experiment on two GPUs in the same node
For this lab, which will be done in teams, the instructors will distribute access to multi-GPU containers running Jupyter Lab. Each team will get its own URL and access token that they will be able to access their Jupyter Lab instance. Your task will be to add [Data Parallelism](https://pytorch.org/tutorials/beginner/blitz/data_parallel_tutorial.html) to your CINIC example, so that it runs on both GPUs.  Does it speed up training?

### Lab 5. Using Distributed Data Parallelism (DDP) to run the experiment on two GPUs in two separate nodes
You will need a pair of VMs for this lab. The idea is to get experience with multinode runs using Pytorch [Distributed Data Parallel](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html). The nodes need to be set up identically for this to work and all ports between them need to be open. IF all goes well, you should be able to start the run on one node and see both GPUs fully utilized.
