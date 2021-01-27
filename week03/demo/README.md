# Introduction to Docker Examples

This file provides a basic introduction to using Docker, with specific examples to using on the Nvidia XAVIER NX.

These examples assume the use of one or more shells open.

## Part 1: Installation
Docker is installed by default as part of the Nvidia Jetpack Install.  For other platforms, see the Docker installation instructions.  See https://docs.docker.com/engine/install/ for installation instructions on non-NX platforms, e.g. macOS x86_64, Windows, Linux (CentOS, Ubuntu, etc.)  Unless noted, these examples will run on any docker example.

Note, at the time of writing, Docker Desktop fo Apple M1 is still a tech preview.  

### Optional for the NX and Linux installations.
By default, Docker is owned by and runs as the user root.  This requires commands to be executed with sudo.  If you don't want to use sudo, a group may be used instead.  This group  group grants privileges equivalent to the root user. For details on how this impacts security in your system, see Docker Daemon Attack Surface (https://docs.docker.com/engine/security/#docker-daemon-attack-surface)
.  The examples will assume this has been done.  If you do not do this, you'll need to prefix the docker commands with `sudo`.

1. Create the group docker.  Note, this group may already exist.
```
sudo groupadd docker
```
2. Add your user to the docker group.
```
sudo usermod -aG docker $USER
```
3. Log out and log back in so that your group membership is re-evaluated.
If testing on a virtual machine, it may be necessary to restart the virtual machine for changes to take effect.

## Part 2: Registries
An image registry provides a means of sharing images.  Registries can be hosted, e.g. DockerHub or NVIDIA's NCG, or may be self hosted.  You'll want to sign up for a free account with DockerHub (https://hub.docker.com).  This will allow you to easily share images. 

See https://docs.docker.com/docker-hub/ for the steps.  Once your account is created, login via the command
```
docker login
```
and follow the prompts.

## Part 3: Hello World

Note, The following will run any docker instance.

This example will run a simple hello world container. You'll start by runninh the command `docker run hello-world`.
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

This command "runs" a container based on the specified image, in this case, an image named hello-world.  
When the command was executed, Docker first checked if the image was availalbe locally, and as it was not, it downloaded it for us.  As we didn't specify the tag, it automatically download the "latest" one.  Next, it started the container, which printed out the message, then exited.  

We can run the command `docker images` to see that we have the hello-world image locally.  The output will look similar to:
```
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
hello-world         latest              a29f45ccde2a        12 months ago       9.14kB
```

The command `docker ps` is used to list containers.  The default command lists only running containers while the -a option is neede to list all containers.

`docker ps`:
```
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```
vs
`docker ps -a`:
```
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                      PORTS               NAMES
697c6c524995        hello-world         "/hello"            10 minutes ago      Exited (0) 10 minutes ago                       tender_galois
```

A stopped container may be deleted with the command `docker rm <container id or container name>`.  Delete your container and verify it has been removed.

When running a container, we can also give it a name with the flag `--name <name>`.  Note, docker provents containers from having duplicate names.  Running hello-world again with this flag:
```
docker run --name helloWorld hello-world
```
Note, the image is not downloaded again, rather the local "cached" image is used.

Run `docker ps -a` again and you should now see something similar to:
```
CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS                          PORTS               NAMES
1ee8c4789e21        hello-world         "/hello"            About a minute ago   Exited (0) About a minute ago                       helloWorld
```

This container can now be deleted with the command `docker rm helloWorld`.

If you don't care to save the container when it exits, docker can automatically delete the container with the option --rm.
Run the command `docker run --name helloWorld --rm hello-world` and then when it exists, rerun `docker ps -a`.  You'll find that the container has been removed.  

When done, you can remove the image with the command `docker rmi hello-world:latest`.  An image may only be deleted when there are no containers using that image.

### Docker command recap
| Command | Description |
| --- | --------- |
| docker ps | Lists all running containers |
| docker ps -a | Lists all containers |
| docker images | Lista all local images |
| docker run  <imageName> | Run an image as a container |
| docker run --name <name> <imageName> | Run an image as a container, using the specified name for the container. |
| docker run --rm <imageName> | Run an image as a conatiner and automatically delete it when it exits. |

## Part 4: Interacting with a container

You'll now see a slightly more interesting example using the Ubuntu base image.  You'll start by running the command `docker pull ubuntu:latest`.  This will explictly download the image for you, making sure you have the most up to date version.  After the download is complete, run the command `docker run --name ubuntu --rm -it ubuntu bash`.  The `-it` option enable interactive mode and allocates a pseudo-TTY.  This allows us to interact with the container process.  The `bash` command tells docker to run the bash shell as the container's process.  This command will give you a shell that looks similar to 
```
root@eb3d250d4de8:/# 
```
Run some commands.  apt-get update && apt-get install vim, etc.  This will work as expected.

As you know, Docker is processed based.  On Linux systems, we can see this from the host by using the ps command.  Note, non-Linux hosts such as macOS run Docker in a Virutal Machine and the host OS cannot see the process.

I've installed VI (apt-get install -y vim) and am editing a file named helloWorld.txt via the command `vi helloWorld.txt`.

```
ps -ef | grep vi
root      6648  5776  0 07:55 pts/0    00:00:00 vi helloWorld.txt
```

As expected, this is just a process!

Exit out of your ubuntu container.

Let's get 2 containers talking to each other!.  In one shell, run the following

```
docker run --name web --hostname web --rm -it ubuntu bash
```

And in a second

```
docker run --name db --hostname db --rm -it ubuntu bash
```

We are using the hostname option to force docker to set the hostname as something recognizable vs the container id.

In the `web` container, let's install ping: `apt-get update && apt-get install iputils-ping -y`

Once installed, let's try to ping `db` with the command `ping db`.  You'll get an error back that says: `ping: db: No address associated with hostname`.  We need to find the container's IP Address; in a third shell, run the command `docker inspect db | grep IPAddress`.  You'll get back a field `IPAddress`; take note of the value.  For example, I get `"IPAddress": "172.17.0.3"`.  Now in web, ping your db's IP Address and you should get a response similar to:
```
root@web:/# ping 172.17.0.3
PING 172.17.0.3 (172.17.0.3) 56(84) bytes of data.
64 bytes from 172.17.0.3: icmp_seq=1 ttl=64 time=0.224 ms
```
Exit out of your 2 containers.

By default, containers can talk by IP Address, but not by name.  While this works, it is brittle and not portable.  There use to be a link option on run, but this was replace by user defined networks.
These user defined networks provide:
- DNS resultion between containers
- Better isolation - only containes attached may communicate with each other.
- Containers can be attached and detached on the fly

You'll create a network with the command `docker network create demo` to create a network named `demo`.  You can verify the network with the command `docker network ls`.  We'll recreate our 2 containers, but this time using our new network.

```
In shell one: 
docker run --name web --hostname web --network demo --rm -it ubuntu bash

In shell two:
docker run --name db --hostname db --network demo --rm -it ubuntu bash

```
In web, install ping again and run the command `ping db`.  This time, you'll get a resopnse!

```
root@web:/# ping db
PING db (172.19.0.3) 56(84) bytes of data.
64 bytes from db.demo (172.19.0.3): icmp_seq=1 ttl=64 time=0.483 ms
64 bytes from db.demo (172.19.0.3): icmp_seq=2 ttl=64 time=0.201 ms
```

Close out your containers and then delete your network with the command `docker network rm demo`.


### Docker command recap
| Command | Description |
| --- | --------- |
| docker ps | Lists all running containers |
| docker ps -a | Lists all containers |
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

## Part 5: More Networking and Persistent files
Note, this is just an example.  For production applications, the files used here should be baked into the image.

In this example, we'll be working with Nginx, a robost HTTP server. You'll launch your instance with the following command `docker run -d --name web --hostname web --rm nginx`.  The `-d` option runs the container in detached mode.  This means the container is running in the background!

```
rdejana@nx:~$ docker run -d --name web --hostname web --rm nginx 
Unable to find image 'nginx:latest' locally
latest: Pulling from library/nginx
c9648d7fcbb6: Pull complete 
af2653e2da79: Pull complete 
1af64ee707c7: Pull complete 
3bdc08a2d3ea: Pull complete 
fed23bd0d00d: Pull complete 
Digest: sha256:4cf620a5c81390ee209398ecc18e5fb9dd0f5155cd82adcbae532fec94006fb9
Status: Downloaded newer image for nginx:latest
2d5a5aa602e5e3c6198ad3ae9733d33255c486fef1ef7a29e56bc42d6cadd9e1
rdejana@nx:~$
```

You'll use the `exec` command to access the container.  Run `docker exec -ti web bash`.  This will attach us to the container and start a bash process for you to interact with.
Once in the command, verify that Nginx is running by curling the server: `curl http://localhost` and you'll see:
```
root@web:/# curl http://localhost
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

Now how to access this container from OUTSIDE the container? Exit out of the shell and stop the container with `docker stop web`.  Recreate the container with the command: 
`docker run -d --name web --hostname web -p 8080:80 --rm nginx`.  The `-p #:#` maps a port on the host, 8080 in this case, to a port in the container, in this case 80.  From a web browser, access you NX, by name or IP on port 8080, eg. http://nx:8080 and you should get back your web page.

You can run the command `docker logs web` to see container's output.
```
docker logs web
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
192.168.1.199 - - [05/Jan/2021:15:51:26 +0000] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15" "-"
```

You'll now customize the HTML page. By default, the HTML files are located in the directory `/usr/share/nginx/html`. You'll want to install VI (or another editor) (apt-get update && apt-get install -y vim).  Change to the HTML dir, and edit the fine index.html replacing the text with:
```
<!DOCTYPE html>
<html>
<head>
<title>Hello World</title>
</head>
<body>
<h1>Hello World from Docker and Nginx!</h1>
</body>
</html>
```
Save the file and access the web page again.  Now stop your container and start it again.  Notice that your changes are now gone.  This is because, when the contaienr is deleted, all of your changes are deleted.  We'll address this by creating a persistent file system.  On your host, create a directory were you'll want to store HTML.  Change to that directory and create the index.html file with the content you used before.  Now launch your container with the following:
```
docker run -d --name web --hostname web -p 8080:80 --rm  -v <your HTML directory>:/usr/share/nginx/html  nginx
```
replacing `<your HTML directory>` with your actual directory.  Access your page again and you'll see your changes!  You've created a container using a bind mount.  This is used to share content from your host to your container.  Another option is to use a volume.  A volume is a more power and portable solution, but one in which the "where" abastraced out. If you are intersted in volumes, see the Docker documentation.

Stop your container.

## Part 6. Building and sharing your own custom image.
Using exiting containers is great, but the Docker also allows you to create and share your own images.  Building your own image starts with a Dockerfile.  In this example, we'll use the following Dockerfile
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
This file is located in this repository under the directory `docker/docker`.

The `FROM` tells Docker which base image we are using.  In this case, you are using the ubuntu 18.04 base image.

`RUN` runs a command in the container.  The run commands here are split for readablity; best practive would be combine them where it makes sense.  Here we are running a set of commands that update the base image, install python3 and install jupyter.  

`WORKDIR` sets up where the container is running from.  The directory is created if it doesn't already exist.

`COPY` enables the copying of files from host to the container.

`CMD` is the command that the container will run at start up.  In this example, it'll start up a notebook.

`#` is a comment.  Comments are not executed by Docker.

To build an image, you'll use the build command.  You'll want to clone this repo and change to the docker directory.

Run `docker build -t myimage .`.  This will create an image named myimage and use the default Dockerfile.  You'll see output like:
```
 docker build --no-cache -t myimage .
Sending build context to Docker daemon  4.608kB
Step 1/10 : FROM ubuntu:18.04
 ---> 2c047404e52d
Step 2/10 : RUN apt-get update && apt-get -y update
 ---> Running in 076f304f5fa0
Get:1 http://security.ubuntu.com/ubuntu bionic-security InRelease [88.7 kB]
Get:2 http://archive.ubuntu.com/ubuntu bionic InRelease [242 kB]
Get:3 http://security.ubuntu.com/ubuntu bionic-security/restricted amd64 Packages [247 kB]
Get:4 http://security.ubuntu.com/ubuntu bionic-security/main amd64 Packages [1845 kB]
Get:5 http://security.ubuntu.com/ubuntu bionic-security/multiverse amd64 Packages [14.9 kB]
Get:6 http://security.ubuntu.com/ubuntu bionic-security/universe amd64 Packages [1376 kB]
Get:7 http://archive.ubuntu.com/ubuntu bionic-updates InRelease [88.7 kB]
Get:8 http://archive.ubuntu.com/ubuntu bionic-backports InRelease [74.6 kB]
Get:9 http://archive.ubuntu.com/ubuntu bionic/main amd64 Packages [1344 kB]
Get:10 http://archive.ubuntu.com/ubuntu bionic/multiverse amd64 Packages [186 kB]
Get:11 http://archive.ubuntu.com/ubuntu bionic/restricted amd64 Packages [13.5 kB]
Get:12 http://archive.ubuntu.com/ubuntu bionic/universe amd64 Packages [11.3 MB]
Get:13 http://archive.ubuntu.com/ubuntu bionic-updates/main amd64 Packages [2272 kB]
...
Removing intermediate container 076f304f5fa0
 ---> c60341f64168
Step 3/10 : RUN apt-get install python3-pip python3-dev build-essential nodejs -y
 ---> Running in 7c6214716125
Reading package lists...
Building dependency tree...
Reading state information...
The following additional packages will be installed:
  binutils binutils-common binutils-x86-64-linux-gnu ca-certificates cpp cpp-7
  dbus dh-python dirmngr dpkg-dev fakeroot file g++ g++-7 gcc gcc-7 gcc-7-base
  gir1.2-glib-2.0 gnupg gnupg-l10n gnupg-utils gpg gpg-agent gpg-wks-client
  gpg-wks-server gpgconf gpgsm libalgorithm-diff-perl
  libalgorithm-diff-xs-perl libalgorithm-merge-perl libapparmor1 libasan4
  libasn1-8-heimdal libassuan0 libatomic1 libbinutils libc-ares2 libc-dev-bin
  -info_1.9-2_amd64.deb ...

...
Step 8/10 : WORKDIR /src/notebooks
 ---> Running in 8bac2a0a6c5c
Removing intermediate container 8bac2a0a6c5c
 ---> d6e882fd43c4
Step 9/10 : COPY notebooks/simple.ipynb ./
 ---> df233fcc6b7c
Step 10/10 : CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
 ---> Running in ea673ebdbbed
Removing intermediate container ea673ebdbbed
 ---> d28014cd5559
Successfully built d28014cd5559
Successfully tagged myimage:latest
skywalker:docker rdejana$ 
```

Go ahead and launch the image with the command `docker run -ti -p 8888:8888 myimage`.  You'll see some info with the token value displayed to stdout.  Use that to login into your notebook.  You can them open simple.ipynb and run it.

You'll now push this image to DockerHub.  Run the command `docker tag myimage <yourdockerid>/myjupyter`, replacing `<yourdockerid>` with your actual value.  For me, it would be `docker tag myimage rdejana/myjupyter`.  You'll them push the image into DockerHub; `docker push rdejana/myjupyter`.
```
skywalker:demo rdejana$ docker tag myimage rdejana/myjupyter
skywalker:demo rdejana$ docker push rdejana/myjupyter
Using default tag: latest
The push refers to repository [docker.io/rdejana/myjupyter]
54601f934e1c: Mounted from rdejana/mytestimagefordocker 
4076f41a98fa: Mounted from rdejana/mytestimagefordocker 
3dc3b21f8df2: Mounted from rdejana/mytestimagefordocker 
62db2e220080: Mounted from rdejana/mytestimagefordocker 
aacaab36a3af: Mounted from rdejana/mytestimagefordocker 
927cc003fdc7: Mounted from rdejana/mytestimagefordocker 
a3e6098f0a63: Mounted from rdejana/mytestimagefordocker 
317dbebecdcd: Mounted from rdejana/mytestimagefordocker 
fe6d8881187d: Mounted from rdejana/mytestimagefordocker 
23135df75b44: Mounted from rdejana/mytestimagefordocker 
b43408d5f11b: Mounted from rdejana/mytestimagefordocker 
latest: digest: sha256:eed27ee55faf1e9fe0a85eadd0e3146fa87876d8e8e25e3fd7c4fddd497a0768 size: 2624
```
Navigate back to DockerHub (https://hub.docker.com) and verify that you can see your image.  Now delete your local image, `docker rmi myimage` and now pull from DockerHub, `docker pull <yourdockerid>/myjupyter`.  You've successfully shared an image!

## Part 7: CPU Architectures
From your NX, run the command `docker pull rdejana/ubuntu`.  Now start a container with the command `docker run -ti --rm rdejana/ubuntu bash`.  Rather than a prompt, you'll get this error message: 
```
standard_init_linux.go:211: exec user process caused "exec format error"
```

If docker inspect is used to find the archicture, you'll see that the image is an amd64 (x86_64).  Running `docker info` will show that your NX uses an aarch64 architecture.  While many DockerHub images provide multiple architectures, you'll need to make sure the image you want to use is supported on your NX.


# GPU

## Part 1: Configure runtime
These must be run on the NX.  You'll want to run with a monitor attached.  Nvidia provides a runtime to enable Docker to use GPUs.  You can verify that the runtime is installed by running the command 
`docker info | grep nvidia`.  You should see `Runtimes: nvidia runc`.  We'll be setting the runtime to be nvidia by default.  Edit the file `/etc/docker/daemon.json`, e.g. sudo `vi /etc/docker/daemon.json`, adding/setting the `default-runtime` to `nvidia`.
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
From a shell, run the following:
```
# Allow containers to communicate with Xorg
$ sudo xhost +si:localuser:root
$ sudo docker run --runtime nvidia --network host -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix nvcr.io/nvidia/l4t-base:r32.3.1

root@nano:/# apt-get update && apt-get install -y --no-install-recommends make g++
root@nano:/# cp -r /usr/local/cuda/samples /tmp
root@nano:/# cd /tmp/samples/5_Simulations/nbody
root@nano:/# make
root@nano:/# ./nbody
```

This will display a N-body simulation, running in a container and displaying on your UI.

## Part 2: TensorFlow
You'll start by pulling the offical Jetson TensorFlow image with the command `docker pull nvcr.io/nvidia/l4t-tensorflow:r32.4.4-tf2.3-py3`.  Details on this image and other images can be found at Nvidia NGC registry, https://ngc.nvidia.com/catalog/containers/nvidia:l4t-tensorflow.  Now start the container `docker run -it --rm  --network host nvcr.io/nvidia/l4t-tensorflow:r32.4.4-tf1.15-py3`.

Once you have the prompt, start python3.  From the python3 prompt, enter the following
 ```
 >>> import tensorflow as tf
 >>> print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
 Num GPUs Available:  1
 ```
You've now used your Nvidia GPU with Tensor from a container!  Other images form Nvidia includ PyTorch with GPU support along with images with scipy and Panadas pre-installed.  


# NX and Kuberenetes

## Part 1: Install and verify Kubernetes
In this demo, we'll expore installing Kubernetes on Jetson Xavier NX and then deploying a simple application.  
We'll be using an approach based on https://thenewstack.io/tutorial-deploying-tensorflow-models-at-the-edge-with-nvidia-jetson-nano-and-k3s/ and using a version of Kubernetes called K3s, a distribution focused a lightweight Kubernetes designed for the Edge.  

You'll first want to make sure that the default runtime for Docker is set to nvidia.  Confirm that the file `/etc/docker/daemon.json` looks like:
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

If changes are needed, you'll need either reboot your NX or restart the docker service.
```
sudo systemctl restart docker
```


To install K3s, run the following: 
```
mkdir $HOME/.kube/
curl -sfL https://get.k3s.io | sh -s - --docker --write-kubeconfig-mode 644 --write-kubeconfig $HOME/.kube/config
```

This installs k3s and has it use a Docker instead of containerd.

After a few minutes, you'll have Kubernetes up and running.
```
kubectl get nodes
NAME   STATUS   ROLES                  AGE   VERSION
nx     Ready    control-plane,master   27s   v1.20.0+k3s2
```

You will create a simple deployment of a Nginx web server.  Create a file named nginx.yaml with the following content:
```
apiVersion: apps/v1 # for versions before 1.9.0 use apps/v1beta2
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 1 # tells deployment to run 1 pod matching the template
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80

```

This file describes what we want running.  A single replica of a Nginx container, which is listening on port 80.

Now run the command `kubectl apply -f nginx.yaml`.  This will create the deployment.  Run the command `kubectl get pods` to watch the containers start up.  Once they are running, run the command `kubectl expose deployment nginx-deployment --port=80 --type=NodePort` to create a service, or a means of accessing, for you deployment.  A NodePort service means we are using a "random" port on the the host.  Run the command `kubectl get service nginx-deployment` to list the service.  Notice the PORT section, and look for `80:####` where `####` is the port your nginx container is exposed on.

To clean up, run `kubectl delete service nginx-deployment` and `kubectl delete deployment nginx-deployment`.  

### Stopping and Starting Kubernetes
Kubernetes is installed as a systemd service and is configured to start automatically.  You can disable this with the following command:
```
sudo systemctl disable k3s
```
The service can be started with the command:
```
sudo systemctl start k3s
```
and stopped with:
```
sudo systemctl stop k3s
```
If k3s doesn't stop cleanling, rebooting will be needed.


## Part 2: Kubernetes and GPU.
Start Kubernetes if needed.  On your NX, create a file named tf.yaml with the following content:
```
apiVersion: v1
kind: Pod
metadata:
  name: tensorflow
spec:
  containers:
  - name: tf
    image: nvcr.io/nvidia/l4t-tensorflow:r32.4.4-tf2.3-py3
    command: [ "/bin/bash", "-c", "--" ]
    args: [ "while true; do sleep 30; done;" ]
```
This will create a simple pod running the the bash shell.

Run `kubectl apply -f tf2.yaml` to create the pod.  Now run `kubectl get pods` and verify that the pod is running.  This may take some time if the image needs to be downloaded.  You'll now "shell" into the container with the command `kubectl exec -it tensorflow -- python3`.

From the prompt, enter the following:
 ```
 >>> import tensorflow as tf
 >>> print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
 Num GPUs Available:  1
 ```

 Exit python and delete your pod with the command `kubectl delete pod tensorflow`  You may now stop Kubernetes or reboot as needed.

