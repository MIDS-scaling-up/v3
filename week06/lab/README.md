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


## Part 1: GStreamer

In this part of the lab, you'll explore using GStreamer, primally via the gst-launch-1.0 tool.  The sections marked `(Audio)` require an audio device, e.g. USB headphones, and may be considered optional.  

### Basics
At its core GStreamer uses pipelines, where a pipelie is a list of elements separated by exclamation marks (!). 


python, opencv, and gstreamer

## Part 2: Quantization
Notebook example

Jetson Inference
