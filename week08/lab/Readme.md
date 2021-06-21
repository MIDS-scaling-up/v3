# Labs 8

This week, the labs will cover aspects of data preparation, using object detection in images as a backdrop.

### Part 1a. Videos from a stationary camera
Videos are made up of frames, and each frame is an image.  But, extracting images from frames is not completely straightforward. We will use the ffmpeg library. Please install it on the machine where you will be doing the lab. Below, we are using Docker:

```
docker run -ti ubuntu bash
# now, run 
# apt update 
# apt install -y ffmpeg
```
Please navigate to https://www.jpjodoin.com/urbantracker/dataset.html . Download sherbrooke_video.avi. This is a 2 min and 13 second video filmed from a traffic camera located at at the Sherbrooke/Amherst intersection in Montreal. 

Create the test directories:

mkdir -p data/ffmepg
mkdir -p data/ffmepg/test1
mkdir -p data/ffmepg/test2
mkdir -p data/ffmepg/test3

If you get errors in the following steps, you can extract to data/ and change the extracted image name pattern.

The first step is to extract a single image from the video.

ffmpeg -i sherbrooke_video.avi -frames:v 1 data/ffmepg/test1/extracted.jpg
the option -frames:v specifies the number of frames to extract and data/ffmepg/test1/extracted.jpg is the output file.
When complete, browser your data directory from your workstation and open up data/ffmepg/test1/extracted.jpg and confirm that extract.


Now you wille extract 100 images from the file using the command ffmpeg -i sherbrooke_video.avi -frames:v 100 data/ffmepg/test2/extract%04d.jpg
With this command, %04d tells ffmpeg to name the extracted images with the serices with a 4 digit pattern, extract0001.jpg, extract0002.jpg, etc. Other numbers may be used, e.g. to use 2 numbers, the pattern would be %02d.


Review the images. How much did the scence change?
Now we'll adjust the frames per second used with the -r option, in this case with 1 frame per second.
ffmpeg -i sherbrooke_video.avi -frames:v 100 -r 1 data/ffmepg/test2/extract%04d.jpg


What's different? What happens if you change r?
Finally, we'll extract all the images with the command ffmpeg -i sherbrooke_video.avi data/ffmepg/test3/extract%04d.jpg


How long did it take?
How many images did you get?
Which is the "best" approach?

### Part 1b. Videos from a moving camera
Download a sample [video dataset](https://w251lab08.s3.us-west-1.amazonaws.com/videos.tar) captured from one of the four user-accessible cameras (the front camera) of Dima's Tesla. A few questions to consider:
* What is the key difference between stationary and moving camera captures?
* What is the resolution?
* What is the frame rate?
* In the light of the previous exercise, what is a good way to extract frames from such a video?

### Part 2. Yolo v5 tutorial
Of the many object detectors, Yolo v5 continues to dominate. Take a look at the [PyTorch object detection models](https://pytorch.org/vision/stable/models.html#object-detection-instance-segmentation-and-person-keypoint-detection) and then glance through [Yolov5 documentation](https://github.com/ultralytics/yolov5)

Open up the [Yolo v5 Colab notebook](https://colab.research.google.com/github/ultralytics/yolov5/blob/master/tutorial.ipynb)  -- if Colab glitches on you, use the [Kaggle variant](https://www.kaggle.com/ultralytics/yolov5) and examine / click though it.  Make sure to create an account on wandb.com. Train the model on the coco128 dataset.

Questions:
* How many files are in the dataset?
* How many annotations?
* How many classes?
* How long does it take to train?
* What is MAP?
* Was transfer learning used in training?
* Are you able to see your experiments on wandb?
* What is the MAP of [Nvidia's SSD300](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/Detection/SSD) recipe?


### Part 3. Training Yolo v5 on custom data
In this section, we will be following the [Roboflow Yolo v5 fine tuning guide] (https://colab.research.google.com/drive/1gDZ2xcTOgR39tGGs-EZ6i3RTs16wmzZQ).  In order to complete this notebook, you will need to log into Roboflow / create an account, so that you are able to download the [BCCD dataset](https://public.roboflow.com/object-detection/bccd). Please follow the guide; training should take 6-10 minutes.  Questions:
* How many classes are in this dataset?
* How many samples?
* Do you get better results with the raw or augmented dataset?

### Part 4. Image annotation
The landscape of image annotators continues to suffer from fragmentation, with solutions rapidly changing and no provider dominating.  For the lab, we will use a very simple system, [MakeSense AI](https://www.makesense.ai/).  Please upload a few dozen images that you extracted in previous sections.  Define a few classes and try annotating. 

Questions:
* How long does it take you to annotate 10-20 images?
* How long would it take to annotate enough images for a reasonable training of Yolo v5?
