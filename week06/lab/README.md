## VNC 
You may use VNC for this lab; if VNC is used, it is strongly recommended to us a reslution less than 4k as resolutions at 4k or higher can cause additional lag.
For example, a resolution of 1600x900 typically decent performance (you may adjust as needed).

Make sure your display cable is not plugged into your and Jetson and from a SSH shell enter: 
```
export DISPLAY=:0
xhost +
sudo xrandr --fb 1600x900
```
![Filter element](images/filter-element.png)

## Part 1: GStreamer

In this part of the lab, you'll explore using GStreamer, primally via the gst-launch-1.0 tool.  

While not covered here, audio is also supported.  See the Gstreamer documentation for examples.
 

### Basics
At its core GStreamer uses pipelines, where a pipelie is a list of elements separated by exclamation marks (!). 

An element can be thought of as a black box with one or more pads, the element's interface to the outside world; data comes in on one side, the data element does something with it and something else comes out the other side.  There are 3 types of elements, source, filter and filter-like, and sink elements.

Source elements generate data for use by a pipeline, for example reading from from a camera or a file. 

![Filter element](images/src-element.png)


Filters and filter-like elements have both input and outputs pads. They operate on data that they receive on their input (sink) pads, and will provide data on their output (source) pads.


Filter-like elements can have any number of source or sink pads.  For example, a demuxer would have one sink pad and several (1-N) source pads, one for each of the  streams contained in the source format. On the other hand, an decoder will only have one source and sink pads.

![Filter element](images/filter-element.png)


![Filter element](images/filter-element-multi.png)


Finally, sink elements are the end of a pipeline; they accept an input and outout to a display, to disk, etc.

![Filter element](images/sink-element.png)


### Pipelines

The first pipeline will be a simple video test image. 
```
gst-launch-1.0 videotestsrc ! xvimagesink
```

This will display a classic "test pattern". The command is composed of two elements, the videotestsrc and a video sink, xvimagesink.

Running `gst-inspect-1.0 videotestsrc` will provide some additional information on the srs and nne of the properies we can set is the `pattern`.
The patterns have an index number or a name and either may be used.  For example both `gst-launch-1.0 videotestsrc pattern=snow ! xvimagesink` and `gst-launch-1.0 videotestsrc pattern=0 ! xvimagesink` produce the same thing.

Explore the various patterns.

The first example demostrated running a single pipeline, but we can do even more.  The following example runs runs two videotestsrc pipelines:
```
gst-launch-1.0 videotestsrc ! xvimagesink videotestsrc pattern=ball ! xvimagesink
```

Nvidia also provides a couple of its own accellerated plugins:

- nv3dsink: a window-based rendering sink, and based on X11
- nveglglessink: EGL/GLES video sink
- nvvidconv: a Filter/Converter/Video/Scaler, converts video from one colorspace to another & Resizes
- nvegltransform: tranforms to the EGLImage format.

Try to use the `nv3dsink`.  A simple approach would be running something similar to `gst-launch-1.0 videotestsrc ! nv3dsink`. 

Does it work...well, it works with JetPack 4.5.X, but doesn't with earlier releases.  You would get an error that says `could not link videotestsrc0 to nv3dsink0`.  

Recall that an element will have pads and that pads have `capabilities` or `caps`.  Caps describe what the pad is able to do/hanlde.

Run `gst-inspect-1.0 videotestsrc` and look at what its source pad (recall source is what the element outputs). 

```
Pad Templates:
  SRC template: 'src'
    Availability: Always
    Capabilities:
      video/x-raw
                 format: { (string)I420, (string)YV12, (string)YUY2, (string)UYVY, (string)AYUV, (string)RGBx, (string)BGRx, (string)xRGB, (string)xBGR, (string)RGBA, (string)BGRA, (string)ARGB, (string)ABGR, (string)RGB, (string)BGR, (string)Y41B, (string)Y42B, (string)YVYU, (string)Y444, (string)v210, (string)v216, (string)NV12, (string)NV21, (string)GRAY8, (string)GRAY16_BE, (string)GRAY16_LE, (string)v308, (string)RGB16, (string)BGR16, (string)RGB15, (string)BGR15, (string)UYVP, (string)A420, (string)RGB8P, (string)YUV9, (string)YVU9, (string)IYU1, (string)ARGB64, (string)AYUV64, (string)r210, (string)I420_10BE, (string)I420_10LE, (string)I422_10BE, (string)I422_10LE, (string)Y444_10BE, (string)Y444_10LE, (string)GBR, (string)GBR_10BE, (string)GBR_10LE, (string)NV16, (string)NV24, (string)NV12_64Z32, (string)A420_10BE, (string)A420_10LE, (string)A422_10BE, (string)A422_10LE, (string)A444_10BE, (string)A444_10LE, (string)NV61, (string)P010_10BE, (string)P010_10LE, (string)IYU2, (string)VYUY, (string)GBRA, (string)GBRA_10BE, (string)GBRA_10LE, (string)GBR_12BE, (string)GBR_12LE, (string)GBRA_12BE, (string)GBRA_12LE, (string)I420_12BE, (string)I420_12LE, (string)I422_12BE, (string)I422_12LE, (string)Y444_12BE, (string)Y444_12LE, (string)GRAY10_LE32, (string)NV12_10LE32, (string)NV16_10LE32 }
                  width: [ 1, 2147483647 ]
                 height: [ 1, 2147483647 ]
              framerate: [ 0/1, 2147483647/1 ]
         multiview-mode: { (string)mono, (string)left, (string)right }
      video/x-bayer
                 format: { (string)bggr, (string)rggb, (string)grbg, (string)gbrg }
                  width: [ 1, 2147483647 ]
                 height: [ 1, 2147483647 ]
              framerate: [ 0/1, 2147483647/1 ]
         multiview-mode: { (string)mono, (string)left, (string)right }
```

Run `gst-inspect-1.0 nv3dsink` and look at its sink pad.
```
Pad Templates:
  SINK template: 'sink'
    Availability: Always
    Capabilities:
      video/x-raw(memory:NVMM)
                 format: { (string)RGBA, (string)BGRA, (string)ARGB, (string)ABGR, (string)RGBx, (string)BGRx, (string)xRGB, (string)xBGR, (string)AYUV, (string)Y444, (string)I420, (string)YV12, (string)NV12, (string)NV21, (string)Y42B, (string)Y41B, (string)RGB, (string)BGR, (string)RGB16 }
                  width: [ 1, 2147483647 ]
                 height: [ 1, 2147483647 ]
              framerate: [ 0/1, 2147483647/1 ]
```
Notice that they don't match; nv3dsink requires `video/x-raw(memory:NVMM)`.  This can be done using the element `nvvidconv`.  Run gst-insect on this element.

Rerun the nv3dsink, this time with nvvidconv, `gst-launch-1.0 videotestsrc ! nvvidconv ! 'video/x-raw(memory:NVMM)' ! nv3dsink`.  Notice the `video/x-raw(memory:NVMM)`; this is setting the capability on nvvidconv.

GStreamer also supports your USB camera.

```
gst-launch-1.0 v4l2src device=/dev/video0 ! xvimagesink
```
or
```
gst-launch-1.0 v4l2src device=/dev/video0 ! nvvidconv ! 'video/x-raw(memory:NVMM)' ! nv3dsink -e
```


Now that we have access to the cameara, we can explore what we can do.  Now the the camera is the limit; if your camera doesn't support 60 FPS and 4K, there is no use asking for it.  

To list all of your cameras, you'll run the command:

```
gst-device-monitor-1.0 Video/Source
```

And you'll get output similar to this (note, we are only concerned with video/x-raw in this case):
```
	name  : UVC Camera (046d:0825)
	class : Video/Source
	caps  : video/x-raw, format=(string)YUY2, width=(int)1280, height=(int)960, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction){ 15/2, 5/1 };
	        video/x-raw, format=(string)YUY2, width=(int)1280, height=(int)720, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction){ 15/2, 5/1 };
	        video/x-raw, format=(string)YUY2, width=(int)1184, height=(int)656, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction){ 10/1, 5/1 };
	        video/x-raw, format=(string)YUY2, width=(int)960, height=(int)720, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction){ 10/1, 5/1 };
	        video/x-raw, format=(string)YUY2, width=(int)1024, height=(int)576, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction){ 10/1, 5/1 };
	        video/x-raw, format=(string)YUY2, width=(int)960, height=(int)544, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction){ 15/1, 10/1, 5/1 };
	        video/x-raw, format=(string)YUY2, width=(int)800, height=(int)600, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction){ 20/1, 15/1, 10/1, 5/1 };
	        video/x-raw, format=(string)YUY2, width=(int)864, height=(int)480, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction){ 20/1, 15/1, 10/1, 5/1 };
	        video/x-raw, format=(string)YUY2, width=(int)800, height=(int)448, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction){ 20/1, 15/1, 10/1, 5/1 };
	        video/x-raw, format=(string)YUY2, width=(int)752, height=(int)416, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction){ 25/1, 20/1, 15/1, 10/1, 5/1 };
	        video/x-raw, format=(string)YUY2, width=(int)640, height=(int)480, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction){ 30/1, 25/1, 20/1, 15/1, 10/1, 5/1 };
	        video/x-raw, format=(string)YUY2, width=(int)640, height=(int)360, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction){ 30/1, 25/1, 20/1, 15/1, 10/1, 5/1 };
	        video/x-raw, format=(string)YUY2, width=(int)544, height=(int)288, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction){ 30/1, 25/1, 20/1, 15/1, 10/1, 5/1 };
	        video/x-raw, format=(string)YUY2, width=(int)432, height=(int)240, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction){ 30/1, 25/1, 20/1, 15/1, 10/1, 5/1 };
	        video/x-raw, format=(string)YUY2, width=(int)352, height=(int)288, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction){ 30/1, 25/1, 20/1, 15/1, 10/1, 5/1 };
	        video/x-raw, format=(string)YUY2, width=(int)320, height=(int)240, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction){ 30/1, 25/1, 20/1, 15/1, 10/1, 5/1 };
	        video/x-raw, format=(string)YUY2, width=(int)320, height=(int)176, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction){ 30/1, 25/1, 20/1, 15/1, 10/1, 5/1 };
	        video/x-raw, format=(string)YUY2, width=(int)176, height=(int)144, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction){ 30/1, 25/1, 20/1, 15/1, 10/1, 5/1 };
	        video/x-raw, format=(string)YUY2, width=(int)160, height=(int)120, pixel-aspect-ratio=(fraction)1/1, framerate=(fraction){ 30/1, 25/1, 20/1, 15/1, 10/1, 5/1 };
	
```

You can see that for this camera, it's format is YUY2, and that our available dimensions and framerates are related. 

For the rest of the camera based examples, you'll need to use values that work with your actual hardware. 

Let's start by asking for 30 FPS.  Note, you'll need to use the` X/1` for framerates.
```
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw,framerate=30/1 ! xvimagesink
```
Notice that the size of the window as changed.  Now what if we want 30 FPS at 1280 x 720?  Let's find out.
```
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw,framerate=30/1,width=1280,height=960 ! xvimagesink
```
and for me, it fails.  If we look above, should be clear why; my camera doesn't support that.  

Let's go the other way and ask for 160x120.
```
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw,framerate=30/1,width=160,height=120 ! xvimagesink
```

And works as expected.   Feel free to explore what your camera can do!


Now what can we do with the video?  Say we want to see the image in grayscale.
```
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw,framerate=30/1 ! videoconvert ! video/x-raw,format=GRAY8 ! videoconvert  ! xvimagesink
```
Why is the extra videoconvert needed?  Try:
```
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw,framerate=30/1 ! videoconvert ! video/x-raw,format=GRAY8  ! xvimagesink
```
Fails as we need to make sure the video is in a format that xvimagesink can understand, e.g. BGRx.


We can do the same with nv3dsink:
```
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw,framerate=30/1 ! nvvidconv ! 'video/x-raw(memory:NVMM)' !  nvvidconv ! 'video/x-raw,format=GRAY8' !  nvvidconv ! 'video/x-raw(memory:NVMM)' ! nv3dsink -e
```

We can also do fun things like flip the image:
```
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw,framerate=30/1,width=160,height=120  ! nvvidconv flip-method=rotate-180 ! 'video/x-raw(memory:NVMM)' ! nv3dsink -e
```

Now let's play with some "special effects".
```
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw, framerate=30/1 ! videoconvert ! warptv ! videoconvert ! xvimagesink

gst-launch-1.0  videotestsrc ! agingtv scratch-lines=15 ! videoconvert ! xvimagesink

```
Inspect both agingtv and warptv to see what other effects can be applied.


Now add some text to the video: 
```
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw, framerate=30/1 ! videoconvert ! textoverlay text="/device/video0" valignment=bottom halignment=left font-desc="Sans, 40" ! xvimagesink
```

Now what having an image be routed to more than one window.  This uses tee and queue.
```
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw, framerate=30/1,width=160,height=120 ! queue ! tee name=t t. ! queue ! xvimagesink sync=false t. ! queue ! videoflip method=horizontal-flip ! xvimagesink sync=false -e
```

We can also overlay images on top of eachother.  We'll take advantage of `nvcompositor` which is accelerated.  

```
gst-launch-1.0 nvcompositor name=mix sink_0::xpos=0 sink_0::ypos=0 sink_0::zorder=10 sink_1::xpos=0 sink_1::ypos=0 ! nvegltransform ! nveglglessink videotestsrc ! nvvidconv ! mix.sink_0 v4l2src device=/dev/video0 ! nvvidconv ! 'video/x-raw(memory:NVMM)' ! mix.sink_1
```


Your Jetson can also encode and decode video with Gstreamer

```
gst-launch-1.0 videotestsrc ! 'video/x-raw, format=(string)I420, width=(int)640, 
height=(int)480' ! omxh264enc ! 'video/x-h264, stream-format=(string)byte-stream' ! h264parse ! omxh264dec ! nvvidconv ! video/x-raw, format=I420 ! nveglglessink -e
```

Take a look at jtop and you can see that hardware accelerators are being used.
```
jtop
```
Let's encode to file.

```
gst-launch-1.0 videotestsrc ! \
  'video/x-raw, format=(string)I420, width=(int)640, \
  height=(int)480' ! omxh264enc ! \
  'video/x-h264, stream-format=(string)byte-stream' ! h264parse ! \
  qtmux ! filesink location=test.mp4 -e
```
Or with your video...
```
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw,framerate=30/1 ! nvvidconv ! omxh264enc ! 'video/x-h264, stream-format=(string)byte-stream' ! h264parse ! qtmux ! filesink location=test.mp4 -e
```

And playing it back is simple:
```
gst-launch-1.0 filesrc location=test.mp4 ! qtdemux ! queue ! h264parse ! nvv4l2decoder ! nv3dsink -e
```

GStreamer can be used to stream media (e.g. create your own IP camera) between devices, however to keep things simple, you'll stream from your Jetson to your Jetson.

This will require two shell windows.


In the first window, run the following: 
```
gst-launch-1.0 videotestsrc  ! nvvidconv ! omxh265enc insert-vui=1 ! h265parse ! rtph265pay config-interval=1 ! udpsink host=127.0.0.1 port=5000 sync=false -e 
```

This starts the "server" broadcasting the packets (udp) to the IP Address 127.0.01 on port 8001. The server broadcasts the stream using RTP that hs h265 ecnoded.

In the second window, run the following: 

```
gst-launch-1.0 udpsrc port=5000 ! application/x-rtp, media=video, encoding-name=H265 ! rtph265depay ! h265parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, format=I420 ! nv3dsink -e
```

This listens for the packets and decodes the RTP stream and displays it on the screen.

Replace videotestsrc with your Jetson's camera.

This is just a very simple introduction to GStreamer.  If you are interested in other ways it can be used on the edge, take a look at Nvidia's DeepStream SDK, a streaming analytic toolkit to build AI-powered applications, which leverages GStreamer.



## Part 2: Quantization


This is a very simple image classification example based on https://github.com/tensorflow/tensorrt/tree/master/tftrt/examples/image_classification updated to run on a Jetson device. You'll learn how to use TensorFlow 2.x to convert a Keras model to three tf-trt models, a fp32, fp16, and int8. A simple set of test images will be used to both validate and benchmark both the native model and the three tf-trt ones.

You'll be using a prebuilt image (rdejana/tf-trt-demo) for this lab.

See docker/ if you'd like to build the image on your own.


```
docker run -it --rm --net=host rdejana/tf-trt-demo:r32.6.1
```



Note, you may need to keep track of the memory status and clear/flush buffers as needed.  As an alternaive, you may run this lab directly from the command line.  See docker/scripts/README.md for the details.


Once the container as started, you'll see output similar to: 

```
[I 21:26:42.668 NotebookApp] Writing notebook server cookie secret to /root/.local/share/jupyter/runtime/notebook_cookie_secret
[I 21:26:43.631 NotebookApp] Serving notebooks from local directory: /app/tf-trt
[I 21:26:43.631 NotebookApp] Jupyter Notebook 6.1.6 is running at:
[I 21:26:43.631 NotebookApp] http://nx:8888/?token=af4be11ce363992a3815f1893de5b4f219940a7fb364040a
[I 21:26:43.631 NotebookApp]  or http://127.0.0.1:8888/?token=af4be11ce363992a3815f1893de5b4f219940a7fb364040a
[I 21:26:43.631 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 21:26:43.647 NotebookApp] 
    
    To access the notebook, open this file in a browser:
        file:///root/.local/share/jupyter/runtime/nbserver-1-open.html
    Or copy and paste one of these URLs:
        http://nx:8888/?token=af4be11ce363992a3815f1893de5b4f219940a7fb364040a
     or http://127.0.0.1:8888/?token=af4be11ce363992a3815f1893de5b4f219940a7fb364040a
```

If you are running on an NX device, navigate to the appropriate URL and open the file tf-trt.ipynb.  If you are using a Nano, open the file tf-trt-nano.ipynb instead.

Once the notebook is open, you may run each piece. Note, the flush.sh script is available to clear cached memory if needed. In addition, the notebook restarts a number of points to clear up memroy.

Think about the changes in peformance.  Feel free to replace the model used with a different one and rerun.
