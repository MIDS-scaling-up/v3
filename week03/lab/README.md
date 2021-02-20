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

Run the command:
```
docker run --name ubuntu --rm -it ubuntu bash
```


 
