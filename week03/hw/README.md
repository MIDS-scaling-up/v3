# Homework 3 - Containers, Kubernetes, and IoT/Edge

## Please note that this homework is graded

### Note: 01/10/2022
If you have upgraded (apt upgrade) your Jetson's installation and are getting an error similar to the following when running docker:
```
docker: Error response from daemon: failed to create shim: OCI runtime create failed: container_linux.go:380: starting container process caused: error adding seccomp filter rule for syscall clone3: permission denied: unknown.
```
See https://forums.developer.nvidia.com/t/docker-isnt-working-after-apt-upgrade/195213/3.  There you'll find the instructions to downgrade and pin the docker version at one that works.  As an alternative, you may add the following option to your run command, `-security-opt seccomp=unconfined`, e.g.
```
docker run -it --rm --runtime nvidia --security-opt seccomp=unconfined --network host nvcr.io/nvidia/l4t-pytorch:r32.6.1-pth1.9-py3
```

### Note: If you do not have a Jetson device.
If you currently do not have a Jetson device, this homework can be done using a virtual machine running on your workstatation.  See lab3's labNoJetson.md for details.  In the instructions, replace Jetson with your local VM.  As OpenCV is most likely not installed in your VM, you may find the cascade file at https://github.com/opencv/opencv/tree/master/data/haarcascades. 

## Instructions

The objective of this homework is to buld a lightweight containerized application pipeline with components running on the edge, your Jetson, and in the the cloud, a VM in AWS.  The application should be writen in a modular/cloud native way so that it could be run on any edge devce or hub and any cloud VM, or even another type of device connected to some type of storage instead of cloud hosted VM.  In addition, the edge application should be deployed using Kubernetes (K3s for example) on your Jetson and the cloud VM components should run using Docker.

You will build an application that is able to capture faces in a video stream coming from the edge, then transmit them to the cloud via MQTT and saving these faces for "long term storage".  For the face detector component, we ask that you use OpenCV and write an application that scans the video frames coming from the connected USB camera for faces. When one or more faces are detected in the frame, the application should cut them out of the frame and send via a binary message each.  Your edge applicaiton should use MQTT as your messaging fabric.  As you'll be treating your Jetson as hub, you'll need a broker installed on the Jetson, and that your face detector sends its messages to this broker first. You'll then need another component that receives these messages from the local broker, and sends them to the cloud [MQTT broker]. Because edge applications often use messages to communicate with other local components, you'll need another local listener that just outputs to its log (standard out) that it has received a face message.

In the cloud, you need to provision a lightweight virtual machine (1-2 CPUs and 2-4 G of RAM should suffice) and run an MQTT broker in a Docker container. As discussed above, the faces will need to be sent here as binary messages.  You'll need a second component here that receives the messages and saves the images to to the s3 Object storage, ideally via [boto](https://pypi.org/project/boto) (e.g. see a code sample here: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html) .

Please don't be intimidated by this homework as it is mostly a learning experience on the building blocks. The concept of the Internet of Things deals with a large number of devices that communicate largely through messaging. Here, we have just one device and one sensor- the camera.  But, we could add a bunch more sensors like microphones, GPS, proximity sensors, lidars, etc.


On the Jetson, we request that you use [Alpine Linux](https://alpinelinux.org/) as the base OS for your MQTT containers as it is frugal in terms of storage. You will need to use Ubuntu as the base for your OpenCV container. Please recall that Jetson devices and Raspberry Pis are both based on the [ARM v8 architecture](https://en.wikichip.org/wiki/arm/armv8) as opposed to Intel x86/64 architecture.

For details on using MQTT with Apline and Ubuntu, refer to Lab 3.

[OpenCV](https://opencv.org/) is THE library for computer vision.  At the moment it has fallen behind the Deep Learning curve, but it could catch up at any moment.  For traditional, non-DL image processing, it is unmatched.


Refer to Lab 3 for how to get started with OpenCV and some addtional hints for getting started with OpenCV in a container are [here](https://github.com/rdejana/w251-hints/tree/master/hw3), if you need them.

### Facial detection with OpenCV 
We suggest that you use a simple pre-trained frontal face HAAR Cascade Classifier [documented here](https://docs.opencv.org/3.4.1/d7/d8b/tutorial_py_face_detection.html).  There is no need to detect eyes,just the face.  Notice how simple it is to use:
```
import numpy as np
import cv2 as cv
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

# gray here is the gray frame you will be getting from a camera
gray = cv.cvtColor(gray, cv.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in faces:
	# your logic goes here; for instance
	# cut out face from the frame.. 
	# rc,png = cv2.imencode('.png', face)
	# msg = png.tobytes()
	# ...
```

```
Note, you can find the OpenCV cascade files on your Jetson in the directory /usr/share/opencv4/haarcascades
```

### Linking containers
On the Jetson, your containers should communicate via Kubernetes services, see Lab 3 for details.  On the cloud side, you should use a user defined network to enable your containers to easily communicate.  Please review the [docker networking tutorial](https://docs.docker.com/network/network-tutorial-standalone/#use-user-defined-bridge-networks).  The idea is that you will need to create a local bridge network and then the containers you will create will join it.

### Overall architecture / flow
Your overall application flow / architecture should be something like: ![this](hw3.png).

### Bonus Points
You can recieve an extra 10 bonus points for using Kubernetes on the cloud side rather than Docker.


### Hints
- Using a USB device from Kubernetes requires a privileged security context.  If you'd like your container to display your camera's images, you'll need to enable host networking and set the DISPLAY env variable.
- To make storing in Object Store easier, look at https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-configure-bucket.html

Review Lab 3!

### Grading/Submission
You are scored based on the following:

- 60 points for a containerized end to end appliation
- 10 points for using a user defined network in the cloud (automatic if using k8s on the cloud side)
- 10 points for using Kubernetes on your Jetson
- 10 points for explaining the MQTT topics and the QoS that you used.
- 10 points for storing your faces in publicly reachable object storage
- 10 bonus points for using Kubernetes instead of Docker on the cloud side.

What to submit to ISVC:

A link to the repository of your for this homework [private repo please] which should include your code, Dockerfiles, Docker command used, and Kubernetes YAML files.  In addition, the answers to the 2 questions (eg. bullet point #4 above) should be included.

A publicly accessble http link to the location of your faces in the object storage. 
