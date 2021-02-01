# Getting started Gstreamer on the Jetson NX

The following is a simple introduction and demo to GStreamer, specfically on the Jetson Xavier NX platform. Additional documentation can be at https://docs.nvidia.com/jetson/l4t/index.html#page/Tegra%20Linux%20Driver%20Package%20Development%20Guide/accelerated_gstreamer.html

The majority of this examples will be use the GStreamer tool gst-launch-1.0.

Note, on Jetson devices the "automatic video sink", `autovideosink` is mapped to a sink that is an overlay.  This means that the sink is not X-windows enabled and doesn't play well with VNC.  As most of these examples are executed on a machine that uses X-windows and potentiall accessed via VNC, this sink will not be used.  Instead, nv3dsink or nveglglessink will be used explictly.


## VNC
This demo may be used via VNC.  If VNC is used, it is strongly recommended to us a reslution less than 4k as resolutions at 4k or higher can cause additional lag when VNC is used.  For example, I typically set my resolution to `1600x900` via the command `xrandr` command and have no display pluged into the nx.

From your a shell:
```
export DISPLAY=:0
xhost +
sudo xrandr --fb 1600x900
```

## JP Version
The recored demo was done using Jetpack 4.4.1 and after the recording, Jetpack 4.5 was released.  There appears to been a change between the versions to either nv3dsink and/or nvvidconv.  Luckly the workaround is easy, replace:
```
nvvidconv ! nv3dsink
```
with
```
nvvidconv ! 'video/x-raw(memory:NVMM)' ! nv3dsink
```
This is backwards compatabile with 4.4.1 and the examples here have been updated to reflect this.

The sink nveglglessink works as expected. 

## Part 1: 
Our first pipeline will be a simple video test image.
``
gst-launch-1.0 videotestsrc ! xvimagesink
``

This will display a classic "test pattern".  The command is composed of two elements, the `videotestsrc` and a video sink, `xvimagesink`.

Running `gst-inspect-1.0 videotestsrc` will provide some additional information on the src.  One of the properies we can set is the pattern.
``
gst-launch-1.0 videotestsrc pattern=snow ! xvimagesink and gst-launch-1.0 videotestsrc pattern=ball ! xvimagesink for example.
``

Nvidia also provides a couple of its own accellerated plugins:
- nv3dsink: a window-based rendering sink, and based on X11
- nveglglessink: EGL/GLES video sink
- nvvidconv: a Filter/Converter/Video/Scaler, converts video from one colorspace to another & Resizes
- nvegltransform: tranforms to the EGLImage format.

Inspecting nv3dsink, we can see that it requires an input of `video/x-raw(memory:NVMM)`.  
This is not someting that videotestsrc outputs, so we'll need to use nvvidconv to convert.
Inspecting this, we can see it can take `video/x-raw` and output  `video/x-raw(memory:NVMM)`.
```
gst-launch-1.0 videotestsrc ! nvvidconv ! 'video/x-raw(memory:NVMM)' ! nv3dsink -e
```

To use nveglglessink, we'll need to use nvvidconv and nvegltransform, to go from NVMM to EGLImage.
```
gst-launch-1.0 videotestsrc ! nvvidconv ! nvegltransform ! nveglglessink -e
```

Which sink to use?  Will it just depends.  xvimagesink is often easier to get going, but the nvidia ones provide additional acceration and perforance.

Note, there are additional Nvidia sinks that may be used, but may not work over technology like VNC, e.g nvdrmvideosink.

## Part 2: USB Camera
Now that we have some experience, we'll add a camera to the fix.  We'll be using a USB camera, which leverages the v4l2src plugin.  While not covered here, if you are using a Raspberry Pi Camera, you would need to use the Nvidia plugin `nvarguscamerasrc`.

This example assumes your camera is using /dev/video0; you may need to adjust depending on your configuration.

As before, we can take advantage of a varity of sinks.
```
gst-launch-1.0 v4l2src device=/dev/video0 ! xvimagesink

gst-launch-1.0 v4l2src device=/dev/video0 ! nvvidconv ! 'video/x-raw(memory:NVMM)' ! nv3dsink -e

gst-launch-1.0 v4l2src device=/dev/video0 ! nvvidconv ! nvegltransform ! nveglglessink -e
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

You can see that for this camera, it's format is YUY2, and that our available dimensions and framerates are related.  Let's start by asking for 30 FPS.  Note, you'll need to use the` X/1` for framerates.
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

We can do the same the Nvidia plugins:
```
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw,framerate=30/1 ! nvvidconv ! 'video/x-raw(memory:NVMM)' !  nvvidconv ! 'video/x-raw,format=GRAY8' !  nvvidconv ! 'video/x-raw(memory:NVMM)' ! nv3dsink -e
```

We can also do fun things like flip the image:
```
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw,framerate=30/1,width=160,height=120  ! nvvidconv flip-method=rotate-180 ! 'video/x-raw(memory:NVMM)' ! nv3dsink -e
```

## Part3: Fun and games

Now let's play with some "special effects".
```
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw, framerate=30/1 ! videoconvert ! warptv ! videoconvert ! xvimagesink

gst-launch-1.0  videotestsrc ! agingtv scratch-lines=15 ! videoconvert ! xvimagesink

```
Now add some text to the video: 
```
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw, framerate=30/1 ! videoconvert ! textoverlay text="/device/video0" valignment=bottom halignment=left font-desc="Sans, 40" ! xvimagesink
```
Now what haveing an image be routed to more than one window.  This uses tee and queue.
```
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw, framerate=30/1,width=160,height=120 ! queue ! tee name=t t. ! queue ! xvimagesink sync=false t. ! queue ! videoflip method=horizontal-flip ! xvimagesink sync=false -e
```

We can also overlay images on top of eachother.  We'll take advantage of `nvcompositor` which is accelerated.  

```
gst-launch-1.0 nvcompositor name=mix sink_0::xpos=0 sink_0::ypos=0 sink_0::zorder=10 sink_1::xpos=0 sink_1::ypos=0 ! nvegltransform ! nveglglessink videotestsrc ! nvvidconv ! mix.sink_0 v4l2src device=/dev/video0 ! nvvidconv ! 'video/x-raw(memory:NVMM)' ! mix.sink_1
```

## Part 4: Encoding and Decoding
The NX can encode and decode video.
```
gst-launch-1.0 videotestsrc ! 'video/x-raw, format=(string)I420, width=(int)640, 
height=(int)480' ! omxh264enc ! 'video/x-h264, stream-format=(string)byte-stream' ! h264parse ! omxh264dec ! nveglglessink -e
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

## Part 5: Streaming

This is a simple streaming example, with both sides running on the NX.  This will require two shell windows.

In the first window, run the following: 
```
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw,framerate=30/1,width=640,height=480 ! nvvidconv ! 'video/x-raw(memory:NVMM), format=NV12' ! nvv4l2h264enc insert-sps-pps=true ! h264parse ! rtph264pay pt=96 ! udpsink host=127.0.0.1 port=8001 sync=false -e
```
This starts the "server" broadcasting the packets (udp) to the IP Address 127.0.01 on port 8001. The server broadcasts the stream using RTP that hs h264 ecnoded.

In the second window, run the following: 
```
 gst-launch-1.0 udpsrc address=127.0.0.1 port=8001 caps='application/x-rtp, encoding-name=(string)H264, payload=(int)96' ! rtph264depay ! queue ! h264parse ! nvv4l2decoder ! nv3dsink -e
```
This listens for the packets and decdes the RTP stream and displays it on the screen.


## Part 6: Python and OpenCV
We can leverage gstreamer from within python and openCV. 

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
You can also leverage features of gstreamer, for example we can add warptv.
```
import numpy as np
import cv2

# use gstreamer for video directly; set the fps
camSet='v4l2src device=/dev/video0 ! video/x-raw, framerate=30/1 ! videoconvert ! warptv ! videoconvert ! appsink'
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

