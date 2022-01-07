# HW02: Docker, Cloud ML Services(Sagemaker) and Pricing

*Complete Lab02 before starting HW02*

# PART1: Docker 101
This is a primer on docker, which in the past few years emerged as the dominant workload management and deployment tool.

Docker - https://www.docker.com/  - is a collection of tools around Linux Containers [which are a lightweight form of virtualization]. 
Linux Containers have been part of the Linux kernel for quite some time now, but the user space tooling has lagged, which provided 
an opportunity for Docker as a company.  Recently, Docker became available on MacOS X and even on Windows 10 Professional or later, in addition
to Linux. Note that while Docker on MacOS X is "native", it requires an underlying hypervisor on Windows. It is important to realize
that a linux container shares the kernel with the underlying VM or host; there is no need to copy the entire OS.  This is why the containers
are very small and light, they are easy to spin up and you can have many of them on devices as small as Raspberry Pi Zero..

#### Installing docker
If you already have docker running on Bastion Host virtual machine, you may skip this step.  However, you may wish to do it if you never installed docker on ubuntu.

Now, login to the Bastion host and follow the official instructions here to install DockerCE on Ubuntu 18:
https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/

# From your workstation
ssh -A ubuntu@YOUR_PUBLIC_EC2_NAME.compute-1.amazonaws.com
```
sudo su
apt-get update
apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
    
# add the docker repo    
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
 
# install it
apt-get update
apt-get install docker-ce
```
#### Running and managing docker containers.
Let us validate that docker is installed:
```
docker run hello-world
```
If this completed successfully, you have successfully got your first docker container running!  Now. let's try to find it:
```
docker ps
```
This command should show you all active docker containers.  At this point, the list should be empty, since the hello-world container exited.  However, the container should still be there:
```
docker ps -a
# Should see something similar to the below:
# CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS                          PORTS               NAMES
# 94a841d96b07        hello-world         "/hello"            About a minute ago   Exited (0) About a minute ago                       elated_brahmagupta
```
Now, let us remove this docker container:
```
docker rm <container_id>
docker ps -a
```

The container should be gone now.

Let's get a ubuntu container going:
```
docker run --name my_ubuntu -ti ubuntu bash
# Your prompt should change to something like
# root@5cf4cef1b2ee:/#
```
This should have downloaded the docker ubuntu image,  created a container called my_ubuntu, started it, and attached a terminal to it.  At this point, you should be inside the container.  The -ti flag connects the current terminal to the container.  Do something inside this container, e.g. 
```
apt-get update
```
Now, let us temporarily disconnect from this container:
```
Ctrl-P Ctrl-Q
```
You should now be back in your VM.  Let's see what's running :
```
docker ps
# you should see your container is actively running.
# CONTAINER ID        IMAGE                              COMMAND              CREATED             STATUS              PORTS                               NAMES
# 30666624229d        ubuntu                             "bash"               17 seconds ago      Up 16 seconds                                           my_ubuntu

```
Now, let us reconnect to the container:
```
docker attach my_ubuntu
```
You should be now back inside the container.  You can play around with it; once you are done, just type
```
exit
```
This should return you from the container and also stop it.  Verify that it is no longer running:
```
docker ps
```
Now, let's start the container:
```
docker start my_ubuntu
docker ps
```
Now, let's re-attach to this container:
```
docker attach my_ubuntu
```
You are back in the container.  Once you are done, disconnect from it (Control-P Control Q), and then remove it as it is running:
```
docker rm -f my_ubuntu
```

#### Using Docker images
Docker containers are spawned from images.  Let's see what images we have locally on our machine:
```
docker images
# should see something like
# ubuntu                  latest               0ef2e08ed3fa        6 months ago        130MB
```
The images are located in docker repositories and are downloaded before the containers are started.  The main docker repository is the Docker Hub: https://hub.docker.com/  Take a moment to browse through the images, do a few searches:

Now, let us download the apache docker image: https://hub.docker.com/_/httpd/
```
docker pull httpd
```
Validate that the image is now available locally, e.g.
```
docker images
```
Now let us start apache.  Note that we are passing port 80 inside the container to port 8003 in our VM and also passing our current
directory to the /usr/local/apache2/htdocs inside the container.
```
docker run -d --name my-apache-app -p8003:80 -v "$PWD":/usr/local/apache2/htdocs/ httpd:2.4
```
Check inbound rules in the default security group to allow this connection to be succesful 

#### Create an inbound rule to allow tcp access into the virtual machine for the following ports
```
aws ec2 authorize-security-group-ingress --group-id  YOUR_PUBLIC_GROUP_ID --protocol tcp --port 8003 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id  YOUR_PUBLIC_GROUP_ID --protocol tcp --port 8800 --cidr 0.0.0.0/0  <used later>
```

Now, let us edit index.html in our current directory and then point our browser to http://ip-of-my-vm:8003  (Use "aws ec2 describe-instances |grep PublicIP" command to get your VM's public IP)
You should be able to see that our http server is running!

#### Using Dockerfiles
We always want to automate deployment to the extent possible.  Let's see how we can create our own docker images.  Create a file called Dockerfile and write to it the following text:
```
# FROM nvidia/cuda
# FROM nvidia/cuda:8.0-cudnn6-devel
# FROM nvidia/cuda:8.0-cudnn5-devel
FROM ubuntu

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    python3-pip \
    python-setuptools \
    python-dev \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install h5py pandas
RUN pip3 install theano

RUN pip3 install --upgrade -I setuptools \
  && pip3 install --upgrade \
    keras

RUN pip3 install  \
    matplotlib \
    seaborn

RUN pip3 install scikit-learn tables
RUN pip3 install --upgrade pip
RUN pip3 install 'ipython<6'

RUN pip3 install jupyter

VOLUME /notebook
WORKDIR /notebook
EXPOSE 8888

ENV KERAS_BACKEND=theano

#  CMD jupyter notebook --no-browser --ip=0.0.0.0 --NotebookApp.token= --allow-root
CMD jupyter notebook --no-browser --ip=0.0.0.0 --allow-root
```
Let's create an image from it:
```
docker build -t test .
```
This will take a minute or two and eventually create a new docker image.  List your docker images to ascertain that it was successfully created.

Now, let's start our test image:
```
docker run --name jupyter -p 8800:8888  -d test
```
In order to access the jupyter notebook, we need to get the access token.  It should be logged to docker stdout, so let's get it:
```
docker logs jupyter
#     Copy/paste this URL into your browser when you connect for the first time,
#   to login with a token:
#        http://0.0.0.0:8888/?token=378684ab93ca16a1348ba2cb874cb52dbc18362fe756648f
```
Now, point your browser to http://my_vm_ip:8800  and use the token to log in.

Once you are all done, stop and remove the container running notebook and terminate the instance to avoid extra charges
You can take an AMI image snapshot before terminating the instance.



# PART2 - Setup and run Sagemaker Example

This HW further builds on using public cloud services with a primer on AWS Sagemaker. Sagemaker is a fully managed Machine Learning Service enabling 
to easily build, train and deploy ML models with an integrated Jupyter Notebook instance.

-   Readup details on Sagemaker. https://docs.aws.amazon.com/sagemaker/latest/dg/ex1-preprocess-data.html

-   Create Sagemaker notebook instance.  https://docs.aws.amazon.com/sagemaker/latest/dg/gs-console.html

-   Create a jupyter notebook and save it. https://docs.aws.amazon.com/sagemaker/latest/dg/ex1-prepare.html

-   Run the end to end Example https://github.com/aws/amazon-sagemaker-examples/blob/master/sagemaker-python-sdk/1P_kmeans_highlevel/kmeans_mnist.ipynb
(This incl. downloading MNIST dataset to your account's default S3 Object storage)

-   Once complete, Login to your account and check the resources the example created

-   Cleanup the environment by deleting the deployed endpoint, Notebook instance and S3 to not incur AWS charges



# PART3 - Pricing
    
#### Spot pricing

As we have limited credit for aws instances, it makes sense to use spot instances which are cheaper than on demand instances.  
With Spot Instances, you pay the Spot price that's in effect for the time period your instances are running. Spot Instance prices are set by Amazon EC2 and adjust gradually based on long-term trends in supply and demand for Spot Instance capacity.   
   
On demand pricing for all instances can be seen at https://aws.amazon.com/ec2/pricing/on-demand/     
At time of writing a t2.large instance costs $0.1008 per Hour in Europe(Ireland) or eu-west-1.    

We can check the equivalent spot price for this instance. Please change the region to your local region - this will shown in `aws configure get region` if you have it set. 
```
aws --region=eu-west-1 ec2 describe-spot-price-history --instance-types t2.large --start-time=$(date +%s) --product-descriptions="Linux/UNIX" --query 'SpotPriceHistory[*].{az:AvailabilityZone, price:SpotPrice}'
```
You should see it is cheaper than the on demand rate, below is an example of one price at time of writing, so over 3 times cheaper!!
```
    {
        "az": "eu-west-1b",
        "price": "0.030200"
    },
```

To provision an instance with spot pricing, create a file in your current directory named `spot-options.json` and place the below inside it, where you configure max price a little above the spot pricing. Spot pricing fluctuates, so leave some buffer. 
```
{
  "MarketType": "spot",
  "SpotOptions": {
    "MaxPrice": "0.05",
    "SpotInstanceType": "one-time"
  }
}
```

Now, start the instance with, 
```
aws ec2 run-instances --image-id ami-0bcc094591f354be2 --instance-type t2.micro --security-group-ids YOUR_PUBLIC_GROUP_ID --associate-public-ip-address --instance-market-options file://spot-options.json --key-name "your_keypair.pem"
```

**Remember to terminate the instance at the end.**

   
### Raise usage limits on your account
Your AWS account has default quotas, formerly referred to as limits, for each AWS service. Unless otherwise noted, each quota is Region-specific. You can request increases for some quotas, and other quotas cannot be increased. Your starting quotas do not include the allowances required for homework 06 and 09, where we will be using more advanced GPU resources. Therefore we need to get the request in early.   
We will be using a [V100](https://www.nvidia.com/en-us/data-center/v100/) in HW06 which is delivered through a p3.2xlarge instance. Please raise a limit request for using 8 VCPUs which will enable a `p3.2xlarge` instance in the region of your choice (preferably your default region in AWS). You can request an on-demand instance. The `Limits` option can be found in the ec2 dashboard of AWS - it is the fourth option, just below `EC2 dashboard`.   
If a quota increase via the service quota console is denied, please try submitting a service quota increase via the support console and provide the reason for the quota increase.   
An approved request is not a prerequisite for completing this homework 02, but please have the request submitted in the `EC2 dashoard`.   
Sample message : 
```
Please update the limit for VCPU on my account to be 8 VCPU for the p3.2xlarge instance type. We are currently running a graded homework in our class at UC Berkeley for the Master in Data Science program about training a Transformer-based Machine Learing Neural network.
```



# PART4 - Turn in 

### Submit text file on class portal homework submission page with answers to the following Questions 
 
-   How can Sagemaker help Data Scientists
  
-   Advantages/Disadvantages of Sagemaker

-   Integration of Sagemaker with other AWS services such as Lambda functions, Kubernetes etc.,

-  When to use what algorithms

-  What are other ML services available from other cloud service providers such as Google, Microsoft, IBM?
