# Lab 3: Containers, Docker, and Kubernetes
This lab will introduce containers, Docker, and the container orchestration system, Kubernetes.  We will use Docker to build and run containers, then explore running the containers with Kubernetes.

This lab is run on the Jetson device using the desktop (via VNC or display); unless noted, all commands are run on your Jetson.

Ensure that you cloned this github repo and are in the directory for this lab (v3/week03/lab/).

This lab may take up to 60 minutes to complete.

Note, if you have upgraded (apt upgrade) your Jetson's installation and are getting an error similar to the following when running docker:
```
docker: Error response from daemon: failed to create shim: OCI runtime create failed: container_linux.go:380: starting container process caused: error adding seccomp filter rule for syscall clone3: permission denied: unknown.
```
See https://forums.developer.nvidia.com/t/docker-isnt-working-after-apt-upgrade/195213/3.  There you'll find the instructions to downgrade and pin the docker version at one that works.  As an alternative, you may add the following option to your run command, `-security-opt seccomp=unconfined`, e.g.
```
docker run -it --rm --runtime nvidia --security-opt seccomp=unconfined --network host nvcr.io/nvidia/l4t-pytorch:r32.6.1-pth1.9-py3
```

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
	
## Getting your Jetson's IP
If your Jetson is wired, e.g. using ethernet, you can find its IP with the command `ifconfig eth0`. If it is wireless, replace eth0 with wlan0. 

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

From your Jetson's display, open a brower and go to http://localhost:8080.  You should be greeted with the Nginx welcome page.  You should notice two new options in with run command, `-d` and `-p`.  First, the `-d` option runs the container in the background. Next, the `-p` is used publish a container's port(s) to the host.  In this case, mapping the host's port 8080 to the container's port 80.  You can also access this container from outside your Jetson; if you were to open a browser on your workstation and to `http://<yourJetsonsIP>:8080`, replacing `<yourJetsonsIP>` with the IP address of your device, you'll once again see the welcome page. 

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
Reboot your Jetson and login when reboot is completed.

This demo wants to use your display, so we'll need to do some additional setup to work.  Note, this requires that you are interacting your Jetson via an attached display or via VNC. If you have a display attached or are using VNC but accessing via an ssh session, you'll first need to run 
```
export DISPLAY=:0
```
To allow containers to communicate with X, run:  
```
sudo xhost +
```
Now run the command (assumes you are using JetPack 4.6):
```
docker run --rm --network host -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix nvcr.io/nvidia/l4t-base:r32.6.1
```
	
If you are running a different version of JetPack, you'll need to use the corresponding tag. 
	
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
Run existing containers from existing images is great, but you can also build your own container images. First you'll build a simple Jupyter Notebook container.  Change to the directory build_example_1 and look at the file `Dockerfile`.
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
Go ahead and launch the image with the command `docker run -ti -p 8888:8888 myimage`. You'll see some info with the token value displayed to stdout. Use that to login into your notebook. You can them open simple.ipynb and run it.

You'll now push this image to DockerHub. If you haven't logged in yet, run the command `docker login` and follow the prompts.  Run the command `docker tag myimage <yourdockerid>/myjupyter`, replacing <yourdockerid> with your actual value. For me, it would be `docker tag myimage rdejana/myjupyter`. You'll them push the image into DockerHub using the command `docker push <yourdockerid>/myjupyter`, e.g. `docker push rdejana/myjupyter`.  When the push is completed, open a broswer and go to `https://hub.docker.com/`, login in, and you should see your newly pushed image.  Note, this image is public and may be used by anybody.  Be careful not to store any credentials in your images!
 
In this next example, we'll build an image with is able to use your USB camera. Change to the directory build_example_2 and review both the Dockerfile and cam.py.

```
FROM ubuntu
  
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt install -y python3-dev python3-pip  python3-opencv vim-tiny  libopencv-dev
RUN pip3 install Cython
RUN pip3 install numpy
# example from https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
COPY cam.py cam.py

CMD ["python3","cam.py"]
```


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

This run command uses two "interesting" options, first is `--device` which allows us to expose a hosts device, in this case, your camera, to the container.  Next is the `--network host`, which attaches the container to host's network.  This is needed for X to work.

If this example doesn't work, confirm your display is setup correctly (e.g. export DISPLAY=:0 and xhost +) and that your camera is on /dev/video0.  If you camera is not using /dev/video0, adjust both cam.py and the --device option to match your machine.


## Part 2: Kubernetes

### Installation

We'll be using an approach based on https://thenewstack.io/tutorial-deploying-tensorflow-models-at-the-edge-with-nvidia-jetson-nano-and-k3s/ and using a version of Kubernetes called K3s, a distribution focused a lightweight Kubernetes designed for the Edge.  

To install K3s, run the following: 
```
sudo apt update
sudo apt install -y curl
	
mkdir $HOME/.kube/
curl -sfL https://get.k3s.io | sh -s - --docker --write-kubeconfig-mode 644 --write-kubeconfig $HOME/.kube/config
```

This installs k3s and has it use a Docker instead of containerd.
If you need to install curl, run the command `sudo apt-get install curl`.

After a few minutes, you'll have Kubernetes up and running.
```
kubectl get nodes
NAME   STATUS   ROLES                  AGE   VERSION
nano     Ready    control-plane,master   27s   v1.20.0+k3s2
```

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
To remove k3s, you can run the following:
```
/usr/local/bin/k3s-uninstall.sh
```

### Getting started with Nginx
You'll explore Kubernetes via the deployment of the http server Nginx.

Create a file named deployNginx.yaml and add the following:
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 2 # tells deployment to run 2 pods matching the template
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
Now create the deployment: 
```
kubectl apply -f deployNginx.yaml
```
Display information about the Deployment:
```
kubectl describe deployment nginx-deployment
```
And you should see something similar to:
```
Name:                   nginx-deployment
Namespace:              default
CreationTimestamp:      Tue, 23 Feb 2021 18:34:45 -0700
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=nginx
Replicas:               2 desired | 2 updated | 2 total | 2 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=nginx
  Containers:
   nginx:
    Image:        nginx:1.14.2
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   nginx-deployment-66b6c48dd5 (2/2 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  32s   deployment-controller  Scaled up replica set nginx-deployment-66b6c48dd5 to 2
```
Now list the Pods created by the deployment:
```
kubectl get pods -l app=nginx
```
And you'll see something like:
```
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-66b6c48dd5-4j2rj   1/1     Running   0          94s
nginx-deployment-66b6c48dd5-892dn   1/1     Running   0          94s
```
Display some informationa about a Pod:
```
kubectl describe pod <pod-name>
```
where <pod-name> is the name of one of your Pods.

Delete one of the pods:
```
kubectl delete pod <pod-name>
```
Now list the Pods again; what happened?

It is nice that the deployment is running, but it would be better to be able to access the web server.  This is will be done via a Kubernetes Service, in this case a NodePort service.  Run the following command to create the service:
```
kubectl expose deployment nginx-deployment --type=NodePort --port=80 --name nginx
```
To find the the port used by the service, run:
```
kubectl get service nginx
```
And you'll get something similar to:
```
NAME    TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
nginx   NodePort   10.106.179.170   <none>        80:30340/TCP   59s
```
In this example, the exposed port is `30340`.  Open a brower to `http://<yourDeviceIP>:<NodePort>` and you should see a welcome page.

To find out which instance served your request, look at the Pod's logs:
```
kubectl logs <podName>
```
You can now delete the resources:
```
kubectl delete service nginx
kubectl delete deployment nginx-deployment
```

### A more interesting example
Now for a more interesting example.  You'll be deploying a simple MQTT broker along with a listener application.


### MQTT 101
MQTT - http://mqtt.org/ is a lightweight messaging protocol for the Internet of Things. You send messages to topics and there are just three simple QoS settings: 0,1, and 2.  Please familiarize yourself with these. Here's a [nice page on MQTT QoS](https://www.hivemq.com/blog/mqtt-essentials-part-6-mqtt-quality-of-service-levels/) and another one [on MQTT topics](https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/) that go over MQTT best practices.


#### Mosquitto
Perhaps the most popular OpenSource MQTT toolkit is called Mosquitto. It is extremely lightweight and fast. 
To install the client on a Debian distro, for instance, you would do this:
```
sudo apt install -y mosquitto-clients
```

Or, if you want to install the broker, you need to do this:
```
sudo apt install -y mosquitto
```

On Alpine Linux, you would instead run:
```
apk add mosquitto
```
	
Note, with the latest version of Alpine, you'll need to supply your own configuation file.  For our use case, this file should contain the following:
	
mosquitto.conf
```
allow_anonymous true
listener 1883 0.0.0.0
```

See the documenation for ways to add and user user credintials.  In addition, when starting the broker, you'll need to use the -c option to specify the conf file.

```
mosquitto -c mosquitto.conf
```
	
To see what packages are available on Alpine linux for Mosquitto, you would do something like [this](https://pkgs.alpinelinux.org/packages?name=mosquitto&branch=edge)


Note that MQTT uses port 1883 for un-encrypted messages.


### Subscribing to messages on an MQTT Broker via mosquitto_sub
To subscribe to a topic tree on an MQTT broker, we do something like this:

```
mosquitto_sub -t applications/in/+/public/# -h <ip address of the MQTT broker>
```

This matches `applications/in/app1/public` as well as `applications/in/app2/public/subtopic`, etc. etc.

### Mosquitto and Kubernetes
With this in mind, we are going to deploy a Mosquitto MQTT broker into Kubernetes, create a service, then use access the broker from outside Kubernetes and then from inside it.

You'll start by building a simple [Alpine Linux](https://alpinelinux.org/) based container.  Alpine is a very lightweight Linux distro that works well on Edge devices.

```
FROM alpine:latest
RUN apk add mosquitto
# Configure to allow remote access
RUN echo "allow_anonymous true" > /etc/mosquitto/mosquitto.conf
RUN echo "listener 1883 0.0.0.0" >> /etc/mosquitto/mosquitto.conf
CMD ["mosquitto","-c","/etc/mosquitto/mosquitto.conf"]
```

Make sure that you specify a tag for your image!


You'll want to build the image and push it into your DockerHub registry, e.g. `docker build -t rdejana/mosquitto:v1 .` and `docker push rdejana/mosquitto:v1`.

Next, you'll want to create a YAML file for the Kubernetes Deployment. Using the following as an example:
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mosquitto-deployment
spec:
  selector:
    matchLabels:
      app: mosquitto
  replicas: 1 # tells deployment to run 1 pods matching the template
  template:
    metadata:
      labels:
        app: mosquitto
    spec:
      containers:
      - name: mosquitto
        image: <yourImageHere>
        ports:
        - containerPort: 1883
```
Use kubectl to deploy the yaml:  
```
kubectl apply -f mosquitto.yaml
```
Confirm the pod is running:


Now to access the broker, you'll need to create a service.  Create a file named mosquittoService.yaml that looks like:
```
apiVersion: v1
kind: Service
metadata:
  name: mosquitto-service
  labels:
    run: mosquitto
spec:
  type: NodePort
  ports:
  - port: 1883
    protocol: TCP
    targetPort: 1883
  selector:
    app: mosquitto
```
   
Again, deploy the yaml.   
```
kubectl apply -f mosquittoService.yaml
```
Run the command `kubectl get service mosquitto-service` and take note of the NodePort Kubernetes assigns.

Let us test and double theck that the service is working. We previously installed the mosquitto-clients package. So, let's start a listener in one terminal window, e.g.:
```
mosquitto_sub -h localhost -p <service port> -t my_topic
```
and submit a message to this topic:
```
mosquitto_pub -h localhost -p <service port> -t my_topic -m "hello mqtt"
```
You should see the message delivered to the listener.  Now you can Control-C out of the listener.


To use the service programmatically, you'll create 2 simple python applications. This can be done using your Jetson device or your local workstation (your choice), but this will assume that you are using your Jetson.  You may want to setup a python virtual env (e.g. python3 -m venv /path/to/new/virtual/environment) for this, but the choice is yours.  To install the MQTT client libraries, run the following, `pip3 install paho-mqtt`.

To create a listener, use the following code in a file named listener.py:
```
import paho.mqtt.client as mqtt


LOCAL_MQTT_HOST="localhost"
LOCAL_MQTT_PORT=<your NodePort>
LOCAL_MQTT_TOPIC="test_topic"

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)
	
def on_message(client,userdata, msg):
  try:
    print("message received: ",str(msg.payload.decode("utf-8")))
    # if we wanted to re-publish this message, something like this should work
    # msg = msg.payload
    # remote_mqttclient.publish(REMOTE_MQTT_TOPIC, payload=msg, qos=0, retain=False)
  except:
    print("Unexpected error:", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message



# go into a loop
local_mqttclient.loop_forever()
```
Set LOCAL_MQTT_PORT to be your NodePort value and if you are not running on your Jetson, set LOCAL_MQTT_HOST to your Jetson's IP address.

Run your listener.

In a second shell, create publisher.py with the following:
```
import paho.mqtt.client as mqtt
  

LOCAL_MQTT_HOST="localhost"
LOCAL_MQTT_PORT=<your NodePort>
LOCAL_MQTT_TOPIC="test_topic"

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

#publish the message
local_mqttclient.publish(LOCAL_MQTT_TOPIC,"Hello MQTT...")
```

Again, set LOCAL_MQTT_PORT to be your NodePort value and if you are not running on your Jetson, set LOCAL_MQTT_HOST to your Jetson's IP address.

Run `python3 publisher.py` and in the listener's shell you should see our message.  You may now stop the listener.

The last part of this lab will be to build and deploy a listener container into kubernetes.  You'll be using Ubuntu for this example.
As you'll be leverageing the Kubernetes DNS to "discover" your broker, you'll want to update LOCAL_MQTT_HOST to be mosquitto-service and LOCAL_MQTT_PORT to 1883.  
```
FROM ubuntu:latest
# this is needed to make sure we can see the log output
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y python3 python3-pip
#RUN a command to intall the MQTT python client 
# Copy your listener.py file into the container
CMD python3 listener.py
```
You'll need to add the command to install the MQTT client and the command to copy your listener file into the container.  Note, you'll also need to push into your DockerHub account.

Create a deployment yaml similar to the following, but adjust to point toward the image you published to DockerHub.
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: listener
spec:
  selector:
    matchLabels:
      app: listener
  replicas: 1 # tells deployment to run 1 pods matching the template
  template:
    metadata:
      labels:
        app: listener
    spec:
      containers:
      - name: listener
        image: <yourImage>
```

Watch the logs of your listener, `kubectl logs -f <podName>` and run your publisher.  You should see that your listener connected via the service name and your message show up!

You can now delete your serivce and deployments.


