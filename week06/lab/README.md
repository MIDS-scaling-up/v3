## VNC 
You may use VNC for this lab; if VNC is used, it is strongly recommended to us a reslution less than 4k as resolutions at 4k or higher can cause additional lag.
For example, 
This demo may be used via VNC. If VNC is used, it is strongly recommended to us a reslution less than 4k as resolutions at 4k or higher can cause additional lag when VNC is used. For example, a resolution of 1600x900 typically decent performance (you may adjust as needed).

Make sure your display cable is not plugged into your and NX and from a SSH shell enter: 
```
export DISPLAY=:0
xhost +
sudo xrandr --fb 1600x900
```
![Filter element](images/filter-element.png)

## Part 1: GStreamer

In this part of the lab, you'll explore using GStreamer, primally via the gst-launch-1.0 tool.  The sections marked `(Audio)` require an audio device, e.g. USB headphones, and may be considered optional.  

### Basics
At its core GStreamer uses pipelines, where a pipelie is a list of elements separated by exclamation marks (!). 

An element can be thought of as a black box with one or more pads, the element's interface to the outside world; data comes in on one side, the data element does something with it and something else comes out the other side.

Source elements generate data for use by a pipeline, for example reading from from a camera or a file. 

![Filter element](images/src-element.png)


Filters and filter-like elements have both input and outputs pads. They operate on data that they receive on their input (sink) pads, and will provide data on their output (source) pads.


Filter-like elements can have any number of source or sink pads.  For example, a demuxer would have one sink pad and several (1-N) source pads, one for each of the  streams contained in the source format. On the other hand, an decoder will only have one source and sink pads.

![Filter element](images/filter-element.png)


![Filter element](images/filter-element-multi.png)


Finally, sink elements are the end of a pipeline; they accept an input and outout to a display, to disk, etc.

![Filter element](images/sink-element.png)




python, opencv, and gstreamer

## Part 2: Quantization
Notebook example

Jetson Inference
