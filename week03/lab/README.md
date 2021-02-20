# Lab 3: Containers, Docker, and Kubernetes
This lab will introduce containers, Dockeer, and the container orchestration system, Kubernetes.  We will use Docker to build and run containers, then explore running the containers with Kubernetes.

This lab is run on the Jetson device using the desktop (via VNC or display); unless noted, all commands are run on your Jetson.

Ensure that you cloned this github repo and are in the directory for this lab (v2/week03/lab/).

## Prerequisites
The following prerequisites are required for this lab:
- Docker is installed on your Jetson device.  This should have been done as part of your Jetpack install.
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

 
