# Homework 3 - Internet of Things 101
This homework builds on on lab 3. It is strongly recommended that lab 3 be completed before starting this homework.

## Please note that this homework is graded



## Instructions
The objective of this homework is to build a lightweight edge application pipeline with components running both on the edge (your Xavier NX) and cloud (a VM in AWS).  We also request that you pay attention to the architecture: write the application in a modular way, and such that it could be run on pretty much any low power edge device or hub (e.g. Raspberry Pi or Raspberry Pi Zero) and any cheap Cloud VM - or, indeed, another low power edge device connected to some kind of storage instead of a Cloud VM.

The overall goal of the assignment is to be able to capture faces in a video stream coming from the edge in real time, transmit them to the cloud in real time, and - for now, just save these faces in the cloud for long term storage.

For this assignment, you will use a microservice architecture, containerizing each piece.  On the NX, you will deploy your containers using Kubernetes and on the AWS VM, you will use Docker.  On the NX, we request that you use [Alpine Linux](https://alpinelinux.org/) as the base OS for your MQTT containers as it is frugal in terms of storage. You will need to use Ubuntu as the base for your OpenCV container. 


For the edge face detector component, we ask that you use OpenCV and write an application that scans the video frames coming from the connected USB camera for faces. When one or more faces are detected in the frame, the application should cut them out of the frame and send via a binary message each.

Because the context of this class is IoT, we request that you use MQTT as the messaging fabric.  So, you will be using an MQTT client to send and receive messages, and MQTT broker as the server component of this architecture.


We also ask that you treat the NX as an IoT Hub.  Therefore, we ask that you install a local MQTT broker in the NX, and that your face detector sends its messages to this broker first.  Then, we ask that you write another component that receives these messages from the local broker, and sends them to the cloud [MQTT broker].

In the cloud, you need to provision a lightweight virtual machine (1-2 CPUs and 2-4 G of RAM should suffice) and run an MQTT broker. As discussed above, the faces will need to be sent here as binary messages.  Another component will need to be created here to receive these binary files and save them to the s3 Object storage. 


Please don't be intimidated by this homework as it is mostly a learning experience on the building blocks. The concept of the Internet of Things deals with a large number of devices that communicate largely through messaging. Here, we have just one device and one sensor - the camera.  But, we could add a bunch more sensors like microphones, GPS, proximity sensors, lidars...

## Alpine Linux and MQTT
Review lab 3 for details on Alpine Linux and MQTT/Mosquitto

To see whether the package you need is available on alpine's package manager, apk, check [this link](https://pkgs.alpinelinux.org/packages)

## OpenCV
[OpenCV](https://opencv.org/) is THE library for computer vision.  At the moment it has fallen behind the Deep Learning curve, but it could catch up at any moment.  For traditional, non-DL image processing, it is unmatched.   
Some hints for getting started with OpenCV in a container are [here](https://github.com/rdejana/w251-hints/tree/master/hw3) and in lab 3.

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
Note, you can find the OpenCV cascade files on the nx in the directory /usr/share/opencv4/haarcascades
```

### Reading video from a USB webcam
This really is super-simple. You read videos one frame at a time.  The example below follows [this tutorial](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html):
```
import numpy as np
import cv2

# 1 should correspond to /dev/video1 , your USB camera. The 0 is reserved for the NX onboard camera
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # We don't use the color information, so might as well save space
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # face detection and other logic goes here
``` 
## Linking containers

Update to use Kubernetes

Talk about how to use the camera and to display from k8s...

As you can see from the architecture diagram below, you will need to make multiple docker containers inside your NX and you need them to work together.  Please review the [docker networking tutorial](https://docs.docker.com/network/network-tutorial-standalone/#use-user-defined-bridge-networks).  The idea is that you will need to create a local bridge network and then the containers you will create will join it, e.g.
```
# Create a bridge:
docker network create --driver bridge hw03
# Create an alpine linux - based mosquitto container:
docker run --name mosquitto --network hw03 -p 1883:1883 -ti alpine sh
# we are inside the container now
# install mosquitto
apk update && apk add mosquitto
# run mosquitto
/usr/sbin/mosquitto
# Press Control-P Control-Q to disconnect from the container

# Create an alpine linux - based message forwarder container:
docker run --name forwarder --network hw03 -ti alpine sh
# we are inside the container now
# install mosquitto-clients
apk update && apk add mosquitto-clients
ping mosquitto
# this should work - note that we are referring to the mosquitto container by name
mosquitto_sub -h mosquitto -t <some topic>
# the above should block until some messages arrive
# Press Control-P Control-Q to disconnect from the container
```


## Overall architecture / flow
Your overall application flow / architecture should be something like ![this](hw03.png).  

On the NX, you should have a mosquitto broker container, based on Alpine linux.  Also, a container for the face detector that connects to the USB webcam, detects faces, and sends them to your internal Mosquitto broker. You should have another container that fetches face files from the internal broker and sends them to the cloud mosquitto broker.  This container should be based on Alpine linux.  In the cloud, you should have a container with a mosquitto broker running inside.  You should also have a container that connects to the cloud mosquitto broker, gets face messages, and puts them into the object storage.

## Submission
Please point us to the repository of your code [private repo please] and provide an http link to the location of your faces in the object storage.  Also, explan the naming of the MQTT topics and the QoS that you used.

## Some hints
1. See Week 1's lab (https://github.com/MIDS-scaling-up/v2/blob/master/week01/lab/Dockerfile.yolov5) for how to install openCV.
2. To make storing in Object Store easier, look at https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-configure-bucket.html


