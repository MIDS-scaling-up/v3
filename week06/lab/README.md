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

For the application programmer, elements are best visualized as black boxes. On the one end, you might put something in, the element does something with it and something else comes out at the other side. For a decoder element, for example, you'd put in encoded data, and the element would output decoded data. In the next chapter (see Pads and capabilities), you will learn more about data input and output in elements, and how you can set that up in your application

Source elements generate data for use by a pipeline, for example reading from disk or from a sound card. Visualisation of a source element shows how we will visualise a source element. We always draw a source pad to the right of the element.

Filters and filter-like elements have both input and outputs pads. They operate on data that they receive on their input (sink) pads, and will provide data on their output (source) pads. Examples of such elements are a volume element (filter), a video scaler (convertor), an Ogg demuxer or a Vorbis decoder.

Filter-like elements can have any number of source or sink pads. A video demuxer, for example, would have one sink pad and several (1-N) source pads, one for each elementary stream contained in the container format. Decoders, on the other hand, will only have one source and sink pads.

Visualisation of a filter element shows how we will visualise a filter-like element. This specific element has one source pad and one sink pad. Sink pads, receiving input data, are depicted at the left of the element; source pads are still on the right.

Visualisation of a filter element with more than one output pad shows another filter-like element, this one having more than one output (source) pad. An example of one such element could, for example, be an Ogg demuxer for an Ogg stream containing both audio and video. One source pad will contain the elementary video stream, another will contain the elementary audio stream. Demuxers will generally fire signals when a new pad is created. The application programmer can then handle the new elementary stream in the signal handler.

Sink elements are end points in a media pipeline. They accept data but do not produce anything. Disk writing, soundcard playback, and video output would all be implemented by sink elements. Visualisation of a sink element shows a sink element.


python, opencv, and gstreamer

## Part 2: Quantization
Notebook example

Jetson Inference
