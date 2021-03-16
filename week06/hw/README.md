# Homework 6

This homework covers some use of GStreamer and model optimization.  It builds on the week 6 lab and completing the lab first is hightly recommended.   

This is an ungraded assignment

## Part 1: GStreamer

1. In the lab, you used the Ndida sink nv3dsink; Nvidia provides a another sink, nveglglessink.  Convert the following sink to use nveglglessink.
```
gst-launch-1.0 v4l2src device=/dev/video0 ! xvimagesink
```

2. What is the difference between a property and a capability?  How are they each expressed in a pipeline?

3. Explain the following pipeline, that is explain each piece of the pipeline, desribing if it is an element (if so, what type), property, or capability.  What does this pipeline do?

```
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw, framerate=30/1 ! videoconvert ! agingtv scratch-lines=10 ! videoconvert ! xvimagesink sync=false
```

4. GStreamer pipelines may also be used from Python and OpenCV.  For example:
```
import numpy as np
import cv2

# use gstreamer for video directly; set the fps
camSet='v4l2src device=/dev/video0 ! video/x-raw,framerate=30/1 ! videoconvert ! video/x-raw, format=BGR ! appsink'
cap= cv2.VideoCapture(camSet)

#cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
```
In the lab, you saw how to stream using Gstreamer.  Using the lab and the above example, write a Python application that listens for images streamed from a Gstreamer pipeline.  You'll want to make sure your image displays in color.

For part 1, you'll need to submit:
- Answer to question 1
- Answer to question 2
- Answer to question 3
- Source code and Gstreamer "server" pipeline used.


## Part 2: Model optimization and quantization

In lab, you saw to how use leverage TensorRT with TensorFlow.  For this homework, you'll look at another way to levarage TensorRT with Pytorch via the Jetson Infernece library (https://github.com/dusty-nv/jetson-inference).

You'll want to train a custom image classification model, using the cat/dog, PlantCLEF, or your own data data.

Like in the lab, you'll want to first baseline the your model, looking a the image of images per second it can classify.  You may train the model using your Jetson device and the Jetson Inference scripts or train on a GPU eanabled server/virtual machine.  Once you have your baseline, follow the steps/examples outlined in the Jetson Inference to run your model with TensorRT (the defaults used are fine) and determine the number of images per second that are processed.

You may use either the container apporach or build the library from source.

For part 2, you'll need to submit:
- The base model you used
- A description of your data set
- How long your trained your model for and what your final accuracy was
- Native Pytorch baseline
- TensorRT performance numbers

