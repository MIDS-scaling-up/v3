# Labs 8

This week, the labs will cover aspects of data preparation, using object detection in images as a backdrop.

### Part 1a. Videos from a stationary camera
Videos are made up of frames, and each frame is an image.  But, extracting images from frames is not completely straightforward. We will use the ffmpeg library. Please install it on the machine where you will be doing the lab. Below, we are using Docker:

```
docker run -ti -v <pathToYourDataDiretory>:/images/data ubuntu bash
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
