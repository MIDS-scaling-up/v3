# Homework 8: Fine tuning an object detector on a custom dataset

This homework is meant to provide a taste of what it's like to create a small domain - specific dataset and use publicly available assets to create a custom models.

Ata high level, the assignment is to annotate some data from the [Tesla cam](https://w251lab08.s3.us-west-1.amazonaws.com/videos.tar) and train a custom object detector on it, proving that you can overfit on it -- e.g. similarly to the coco128 dataset, you can train and validate on the same dataset, making sure that your mAP@.5 is modest, over 0.05 (5%)

Notes:
* Peruse [Yolo v5 best practices](https://docs.ultralytics.com/tutorials/training-tips-best-results/)
* Annotate at least 100 images. Recommended: 300
* Look for large objects, e.g. the file like `2021-06-13_19-22-13-front.mp4`
* Create at least two classes. Recommended: 'Car' and 'Truck'
* Feel free to use [MakeSense AI](https://www.makesense.ai/) or [Label Studio](https://labelstud.io/). Recommended: MakeSense AI for simplicity, as in case of Label Studio, you'll need to convert your labels from VoC format into Yolo format.
* Recommended: use Active Learning
* Your annotation folder should contain two subfolders: "images" and "labels". Recommended: call your encapsulating folder something like "hw08" and place it in a folder at the same level as yolov5.
* Create hw08.yaml per the template below.
* Train for as many epochs as needed to cross the 0.05 mAP@.5


```
# hw08.yaml


# train and val data as 1) directory: path/images/, 2) file: path/images.txt, or 3) list: [path1/images/, path2/images/]
train: ../hw08/images/  
val: ../hw08/images/  

# number of classes
nc: 2

# class names
names: [ 'car', 'truck' ]
```
Due before week 9 session begins

Credit / no credit only
