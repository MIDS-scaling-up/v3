# Homework 8: Fine tuning an object detector on a custom dataset

This homework is meant to provide a taste of what it's like to create a small domain - specific dataset and use publicly available assets to create a custom models.

Part 1a. Videos from a stationary camera
Videos are made up of frames, and each frame is an image. But, extracting images from frames is not completely straightforward. We will use the ffmpeg library. Please install it on the machine where you will be doing the lab. Below, we are using Docker:

docker run -ti ubuntu bash
# now, run 
apt update 
apt install -y ffmpeg
Note, if you are using Docker, you'll want to use a volume on the host system to make it easier to see your output. This can be done by adding -v <hostDir>:<containerDir> (example: sudo docker run -ti -v ~/videos-output:/var/log/video ubuntu /bin/bash ).

Please navigate to https://www.jpjodoin.com/urbantracker/dataset.html . Download sherbrooke_video.avi. This is a 2 min and 13 second video filmed from a traffic camera located at at the Sherbrooke/Amherst intersection in Montreal.

Create the test directories:

mkdir -p data/ffmpeg
mkdir -p data/ffmpeg/test1
mkdir -p data/ffmpeg/test2
mkdir -p data/ffmpeg/test3
If you get errors in the following steps, you can extract to data/ and change the extracted image name pattern.

The first step is to extract a single image from the video.

ffmpeg -i sherbrooke_video.avi -frames:v 1 data/ffmepg/test1/extracted.jpg the option -frames:v specifies the number of frames to extract and data/ffmepg/test1/extracted.jpg is the output file. When complete, browser your data directory from your workstation and open up data/ffmepg/test1/extracted.jpg and confirm that extract.

Now you wille extract 100 images from the file using the command ffmpeg -i sherbrooke_video.avi -frames:v 100 data/ffmepg/test2/extract%04d.jpg With this command, %04d tells ffmpeg to name the extracted images with the serices with a 4 digit pattern, extract0001.jpg, extract0002.jpg, etc. Other numbers may be used, e.g. to use 2 numbers, the pattern would be %02d.

Review the images. How much did the scence change? Now we'll adjust the frames per second used with the -r option, in this case with 1 frame per second. ffmpeg -i sherbrooke_video.avi -frames:v 100 -r 1 data/ffmepg/test2/extract%04d.jpg

What's different? What happens if you change r? Finally, we'll extract all the images with the command ffmpeg -i sherbrooke_video.avi data/ffmepg/test3/extract%04d.jpg

How long did it take? How many images did you get? Which is the "best" approach?

Part 1b. Videos from a moving camera
Download a sample video dataset captured from one of the four user-accessible cameras (the front camera) of Dima's Tesla. A few questions to consider:

What is the key difference between stationary and moving camera captures?
What is the resolution?
What is the frame rate?
In the light of the previous exercise, what is a good way to extract frames from such a video?

At a high level, the assignment is to annotate some data from the [Tesla cam](https://w251lab08.s3.us-west-1.amazonaws.com/videos.tar) and train a custom object detector on it, proving that you can overfit on it -- e.g. similarly to the coco128 dataset, you can train and validate on the same dataset, making sure that your mAP@.5 is modest, over 0.25 (25%)

Notes:
* Let us use the EfficientDet detector we used in the lab
* Annotate about 300 images
* Look for large objects, e.g. the file like `2021-06-13_19-22-13-front.mp4`
* Create at least two classes. Recommended: 'Car' and 'Truck'
* Feel free to use [MakeSense AI](https://www.makesense.ai/) or [Roboflow](http://roboflow.com/).Make sure your annotations are (or converted to) the coco format.
* Recommended: use Active Learning
* Train for as many epochs as needed to cross the 0.25 mAP@.5

Due before week 9 session begins

Credit / no credit only
