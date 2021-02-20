# Lab 3: Containers, Docker, and Kubernetes
This lab will introduce containers, Dockeer, and the container orchestration system, Kubernetes.  We will use Docker to build and run containers, then explore running the containers with Kubernetes.

This lab is run on the Jetson device using the desktop (via VNC or display); unless noted, all commands are run on your Jetson.

Ensure that you cloned this github repo and are in the directory for this lab (v2/week03/lab/).

## Prerequisites
The following prerequisites are required for this lab:
- Docker is installed on your Jetson device.  This should have been done as part of your Jetpack install.
- USB camera is plugged in and available.
- A DockerHub account.  DockerHub will be used as your registry, a place to publish and share images.  You may register for the account at https://hub.docker.com.
- Configure Docker group (optional). By default, Docker is owned by and runs as the user root. This requires commands to be executed with sudo. If you don't want to use sudo, a group may be used instead. This group group grants privileges equivalent to the root user. For details on how this impacts security in your system, see Docker Daemon Attack Surface (https://docs.docker.com/engine/security/#docker-daemon-attack-surface) . The examples will assume this has been done. If you do not do this, you'll need to prefix the docker commands with sudo.

Create the group docker. Note, this group may already exist.
```
sudo groupadd docker

```
Add your user to the docker group.
```
sudo usermod -aG docker $USER
```
Log out and log back in so that your group membership is re-evaluated.

## Useful Docker commands
Not all commands may be covered in this lab.

| Command | Description |
| --- | --------- |
| docker ps | Lists all running containers |
| docker ps -a | Lists all containers |
| docker pull <image> | Pull an image from a registry |
| docker images | Lista all local images |
| docker run  <imageName> | Run an image as a container |
| docker run --name <name> <imageName> | Run an image as a container, using the specified name for the container. |
| docker run --rm <imageName> | Run an image as a conatiner and automatically delete it when it exits. |
| docker network create <name> | Create a user defined network |
| docker network ls | List networks |
| docker network rm <name> | Delete a network |
| docker run -it ... | Enable the abiliy to interact with a container via stdin and stdout |
| docker run --hostname ... | Set the hostname of the container |
| docker run --network ... | Set the container's network |
| docker inspect <name> | Return low-level information on Docker objects |
| docker rm <name> | Delete a container |
| docker rmi image name | Delete an image from the local cache |

## Part 1: Docker

This section of the lab will introduce Docker.  

### Hello World
As is the custom in Computer Science, we'll start with `hello world`.  
Run the command: 
```
docker run --rm hello-world
```
If things are correctly installed, you'll see an output similar to:
```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
256ab8fe8778: Pull complete 
Digest: sha256:1a523af650137b8accdaed439c17d684df61ee4d74feac151b5b337bd29e7eec
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (arm64v8)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
 ```
 You have successfully run your first container!
 Note, the `--rm` option deletes the container when its execution is finished.
 
 ### Interacting with a container
The hello world container is nice to demonstrate that Docker is running, but it doesn't really show anything interesting.  Let's start a container rather than have it just display a message, let's interact with it.

You'll start by running the command:
```
docker pull ubuntu:latest
```  
This will explictly download the image for you, making sure you have the most up to date version.  After the download is complete, run the command:

```
docker run --name ubuntu --hostname ubuntu --rm -it ubuntu bash
```
The `-it` option enable interactive mode and allocates a pseudo-TTY.  This allows us to interact with the container process.  The `--hostname` option allows us to pass in the hostname for the container. Note, this is different from just setting the container's name via `--name`. The `bash` command tells docker to run the bash shell as the container's process.   This command will give you a shell that looks similar to:

```
root@ubuntu:/# 
```

From a separate shell on your Jetson, run the command:
```
docker ps
```
You should see something similar to
```
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
619212052b2d        ubuntu              "bash"              4 seconds ago       Up 3 seconds                            ubuntu
```
This lists the containers currently running on your machine.

In the container's shell, run some commands,  apt-get update && apt-get install vim, etc.  All of these command will work as exected.

When complete, type `exit` to leave your container.

### Accessing containers over the network
In this example, we'll be working with Nginx, a robost HTTP server. 

Run the command: 
```
docker run -d --name web --hostname web --rm -p 8080:80 nginx
```

From your Jetson's diplsay, open a brower and go to http://localhost:8080.  You should be greeted with the Nginx welcome page.  You should notice two new options in with run command, `-d` and `-p`.  First, the `-d` option runs the container in the background. Next, the `-p` is used publish a container's port(s) to the host.  In this case, mapping the host's port 8080 to the container's port 80.  You can also access this container from outside your Jetson; if you were to open a browser on your workstation and to `http://<yourJetsonsIP>:8080`, replacing `<yourJetsonsIP>` with the IP address of your device, you'll once again see the welcome page. 

To stop your container, run the command `docker stop web`.

You can use other ports as well, for example, you could also have used port 80, e.g. `docker run -d --name web --hostname web --rm -p 80:80 nginx`. You would then access the container via port 80.

### Using the GPU
Nvidia has provided a runtime that enables Docker containers to leverage the GPU.  This runtime is not the default one, however for our use, let's make it the default.

Edit the file `/etc/docker/daemon.json`, e.g. sudo `vi /etc/docker/daemon.json`, adding/setting the `default-runtime` to `nvidia`.
```
{
    "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    },
    "default-runtime": "nvidia"
}
```
Reboot your NX and login when reboot is completed.

This demo wants to use your display, so we'll need to do some additional setup to work.  Note, this requires that you are interacting your Jetson via an attached display or via VNC. If you have a display attached or are using VNC but accessing via an ssh session, you'll first need to run 
```
export DISPLAY=:0
```
To allow containers to communicate with X, run:  
```
sudo xhost +
```
Now run the command (Note, this assumes JetPack 4.5):
```
docker run --rm --network host -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix nvcr.io/nvidia/l4t-base:r32.5.0
```
Once in the shell, run the following commands:
```
apt-get update && apt-get install -y --no-install-recommends make g++
cp -r /usr/local/cuda/samples /tmp
cd /tmp/samples/5_Simulations/nbody
make
./nbody
```
This will display a GPU powered N-body simulation, running in a container and displaying on your UI.  Close the window and exit out of your container.

### Building containers
Run existing containers from existing images is great, but you can also build your own container images. First you'll build a simple Jupyter Notebook container.  Change to the director build_example_1 and look at the file `Dockerfile`.
```
# Using ubuntu 18.04 as base image
FROM ubuntu:18.04
# update the base image
RUN apt-get update && apt-get -y update
# install 
RUN apt-get install python3-pip python3-dev build-essential nodejs -y
# make python3 -> python
RUN ln -s /usr/bin/python3 /usr/local/bin/python 
# update pip
RUN pip3 install --upgrade pip
# install jupyter and lab
RUN pip3 install jupyter
RUN pip3 install jupyterlab
# set our workdir
WORKDIR /src/notebooks
COPY notebooks/simple.ipynb ./
# Setup which command to run...
# This runs jup notebook 
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
# This runs jup lab
#CMD ["jupyter", "lab", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
```
This is file contains the commands that will be used to build a custom image.  

The `FROM` tells Docker which base image we are using. In this case, you are using the ubuntu 18.04 base image.

`RUN` runs a command in the container. The run commands here are split for readablity; best practive would be combine them where it makes sense. Here we are running a set of commands that update the base image, install python3 and install jupyter.

`WORKDIR` sets up where the container is running from. The directory is created if it doesn't already exist.

`COPY` enables the copying of files from host to the container.

`CMD` is the command that the container will run at start up. In this example, it'll start up a notebook.

`#` is a comment. Comments are not executed by Docker.

To build the image, you'll use the command `docker build -t myimage .` where the `-t` is used to specify the image's name.  When the build is complete, you'll see an output similar to 
```
Step 10/10 : CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
 ---> Running in 8158469d5a5b
Removing intermediate container 8158469d5a5b
 ---> 2ddce619ee6c
Successfully built 2ddce619ee6c
Successfully tagged myimage:latest
```
Go ahead and launch the image with the command docker run -ti -p 8888:8888 myimage. You'll see some info with the token value displayed to stdout. Use that to login into your notebook. You can them open simple.ipynb and run it.

You'll now push this image to DockerHub. If you haven't logged in yet, run the command `docker login` and follow the prompts.  Run the command `docker tag myimage <yourdockerid>/myjupyter`, replacing <yourdockerid> with your actual value. For me, it would be `docker tag myimage rdejana/myjupyter`. You'll them push the image into DockerHub using the command `docker push <yourdockerid>/myjupyter`, e.g. `docker push rdejana/myjupyter`.  When the push is completed, open a broswer and go to `https://hub.docker.com/`, login in, and you should see your newly pushed image.  Note, this image is public and may be used by anybody.  Be careful not to store any credentials in your images!
 
In this next example, we'll build an image with is able to use your USB camera. Change to the directory build_example_2 and review both the Dockerfile and cam.py.
```
# cam.py
# this is from https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
import numpy as np
import cv2


# the index depends on your camera setup and which one is your USB camera.
# you may need to change to 1 depending on your local config
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
```
To build the container, run the command:
```
docker build -t camera .
```
To run the container: 
```
docker run -it --rm --device /dev/video0 --network host -e DISPLAY=$DISPLAY camera:latest
```

This run command uses two "interestig" options, first is `--device` which allows us to expose a hosts device, in this case, your camera, to the container.  Next is the `--network host`, which attaches the container to host's network.  This is needed displaying.

If this example doesn't work, confirm your display is setup correctly (e.g. export DISPLAY=:0 and xhost +) and that your camera is on /dev/video0.  If you camera is not using /dev/video0, adjust both cam.py and the --device option to match your machine.
```
 
