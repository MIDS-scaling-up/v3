Part 1: GStreamer

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
In the lab, you saw how to stream using Gstreamer.  Using the lab and the above example, write a Python application that listens for images streamed from a Gstreamer pipeline.


- Quantize a model
- using the base model of your choice, 
