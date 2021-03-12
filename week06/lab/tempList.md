gst-launch-1.0 audiotestsrc ! alsasink

gst-inspect-1.0 audiotestsrc

gst-launch-1.0 audiotestsrc freq=500 ! alsasink

gst-launch-1.0 audiotestsrc freq=500 ! alsasink

gst-inspect-1.0 audiotestsrc

gst-launch-1.0 audiotestsrc freq=500 ! audio/x-raw, format=U8 ! alsasink

gst-launch-1.0 audiotestsrc freq=500 ! audio/x-raw, format=U18LE ! alsasink

gst-launch-1.0 audiotestsrc freq=500 ! audio/x-raw, format=U18LE ! audioconvert ! audio/x-raw, format=U8 ! alsasink

gst-launch-1.0 videotestsrc ! ximagesink

gst-inspect-1.0 videotestsrc

gst-launch-1.0 videotestsrc pattern=11 ! ximagesink

gst-launch-1.0 videotestsrc pattern=0 ! video/x-raw, format=BGR ! ximagesink

gst-inspect-1.0 autovideoconvert

gst-launch-1.0 videotestsrc pattern=0 ! video/x-raw, format=BGR ! autovideoconvert ! ximagesink

gst-launch-1.0 videotestsrc pattern=0 ! video/x-raw, format=BGR ! autovideoconvert ! videoconvert ! video/x-raw, width=1280, height=960 !  ximagesink 

gst-launch-1.0 videotestsrc pattern=0 ! video/x-raw, format=BGR ! autovideoconvert ! videoconvert ! video/x-raw, width=1280, height=960, framerate=30/1 !  ximagesink

gst-launch-1.0 videotestsrc pattern=0 ! video/x-raw, format=BGR ! autovideoconvert ! videoconvert ! video/x-raw, width=1280, height=960, framerate=1/1 !  ximagesink

gst-launch-1.0 nvarguscamerasrc ! autovideo

gst-launch-1.0 nvarguscamerasrc !  nvvidconv flip-method=2 ! video/x-raw,width=1280,height=840 ! autovideoconvert  !  ximagesink

gst-launch-1.0 nvarguscamerasrc ! "video/x-raw(memory:NVMM),width=3264,height=2464,format=NV12,framerate=21/1" !  nvvidconv flip-method=2 ! video/x-raw,width=640,height=480 ! autovideoconvert  !  ximagesink

gst-launch-1.0 nvarguscamerasrc ! "video/x-raw(memory:NVMM),width=3264,height=2464,format=NV12,framerate=21/1" !  nvvidconv flip-method=2 ! video/x-raw,width=640,height=480 ! autovideoconvert  ! agingtv ! ximagesink

gst-launch-1.0 nvarguscamerasrc ! "video/x-raw(memory:NVMM),width=3264,height=2464,format=NV12,framerate=21/1" !  nvvidconv flip-method=2 ! video/x-raw,width=640,height=480 ! autovideoconvert  ! agingtv ! ximagesink


gst-launch-1.0 nvarguscamerasrc ! "video/x-raw(memory:NVMM),width=3264,height=2464,format=NV12,framerate=21/1" !  nvvidconv flip-method=2 ! video/x-raw,width=1280,height=960 ! autovideoconvert  ! agingtv ! coloreffects preset=sepia ! ximagesink

gst-launch-1.0  v4l2src device=/dev/video1 ! xvimagesink

gst-launch-1.0  v4l2src device=/dev/video1 ! video/x-raw,framerate=20/1,width=864,height=480 ! xvimagesink
