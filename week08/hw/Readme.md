# Homework 8: Fine tuning an object detector on a custom dataset

This homework is meant to provide a taste of what it's like to create a small domain - specific dataset and use publicly available assets to create a custom models.

At a high level, the assignment is to annotate some data from the [Tesla cam](https://w251lab08.s3.us-west-1.amazonaws.com/videos.tar) (You will need to convert the video into images to use the images for annotation, please look at the instructions [here](https://github.com/MIDS-scaling-up/v3/blob/main/week08/lab/Readme.md#part-1a-videos-from-a-stationary-camera)) and train a custom object detector on it, proving that you can overfit on it -- e.g. similarly to the coco128 dataset, you can train and validate on the same dataset, making sure that your mAP@.5 is modest, over 0.25 (25%)

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
