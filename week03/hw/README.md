# Homework 3 - ML pipelines and IoT/Edge

 :warning: **Please note that this homework is graded**

## Instructions

The objective of this homework is to buld a lightweight containerized application pipeline with components running on the edge (emulated by capturing a video/set of videos) and in the the cloud, a VM in the cloud (AWS).  The application should be writen in a modular/cloud native way so that it could be run on any edge devce or hub and any cloud VM, or even another type of device connected to some type of storage instead of cloud hosted VM.   

Firstly, you capture videos with your smartphone / tablet / digital camera. We recommend that you do something that is connected to your hobbies or a problem of interest. You can be creative - e.g., you can put a camera next to a bird feeder in your backyard. You can record fish or turtle in your aquarium. You can record yourself doing fitness exercises. You can record what your dog is doing while you're not at home. You can record what's happening in your fridge. You can record a sports game with your friends (but don't forget to ask for their permission 😉). You can record your collection of Star Track figurines, etc. This video stream is your data in this assignment. 

Next, you will build an application that is able to process this video stream coming from the edge, use an object detection model to identify frames with specific objects of interest, then transmit them to the cloud  and save for "long term storage".  For the object detector component, we ask that you use DETR neural netwrok and write an application that scans the video frames for objects that are relevant to your task. Depending on the domain that you chose, it may be a dog, a bird, a squirrel, a human, etc. When one or more objects of interest are detected in the frame, the application should cut them out of the frame and send via a binary message each.   

In the cloud, you need to provision a lightweight virtual machine (1-2 CPUs and 2-4 G of RAM should suffice). As discussed above, the images will need to be sent here as binary messages.  You'll need a second component here that receives the messages and saves the images to to the s3 Object storage, ideally via [boto](https://pypi.org/project/boto) (e.g. see a code sample here: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html) .

Please don't be intimidated by this homework as it is mostly a learning experience on the building blocks. The concept of the Internet of Things deals with a large number of devices that communicate largely through messaging. Here, we have just one device and one sensor- the camera.  But, we could add a bunch more sensors like microphones, GPS, proximity sensors, lidars, etc.

[DETR-ResNet-50](https://huggingface.co/facebook/detr-resnet-50)  is [the most downloadable](https://huggingface.co/models?pipeline_tag=object-detection&sort=downloads) ML model for object detection task on Hugging Face 🤗 at the moment, which is one of the reasons why we want you to get hands-on experience with it. More on reasons later...

### Object detection with DETR 
We suggest that you use a simple pre-trained frontal version of the model [documented here](https://huggingface.co/docs/transformers/model_doc/detr).  Notice how simple it is to use, despite being quite complex inside:
```
from transformers import DetrFeatureExtractor, DetrForObjectDetection
import torch
from PIL import Image
import requests

url = "http://images.cocodataset.org/val2017/000000039769.jpg"
image = Image.open(requests.get(url, stream=True).raw)

feature_extractor = DetrFeatureExtractor.from_pretrained("facebook/detr-resnet-50")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

inputs = feature_extractor(images=image, return_tensors="pt")
outputs = model(**inputs)

# convert outputs (bounding boxes and class logits) to COCO API
target_sizes = torch.tensor([image.size[::-1]])
results = feature_extractor.post_process(outputs, target_sizes=target_sizes)[0]

for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    # let's only keep detections with score > 0.9
    if score > 0.9:
        print(
            f"Detected {model.config.id2label[label.item()]} with confidence "
            f"{round(score.item(), 3)} at location {box}"
        )
```
You can learn more details about DETR in [this original article](https://arxiv.org/abs/2005.12872).

### Overall architecture / flow
Your overall application flow / architecture should be something like: ![this](https://github.com/alsavelv/v3/blob/MIDS-scaling-up/v4/week03/hw/Pipeline.PNG). 

### Hints
- To make storing in Object Store easier, look at https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-configure-bucket.html
- Depending on the nature of your video stream, optimal video length and sampling frequency may vary. For example, if you are recording a hyper-active puppy, you may want a frame every few millsecounds; but if you record a sloth, this is a different situation:

![flash](https://media.tenor.com/lWXg5ivpQUQAAAAC/zootopia-flash.gif)
 
### Grading/Submission
You are scored based on the following:

- 10 points for problem statement.
- 15 points for curating and sharing videos.
- 50 points for end-to-end ML pipeline.
- 15 points for storing your faces in publicly reachable object storage.
- 10 points for the write-up about the pipeline output.
- 10 bonus points 🎉🎉 for trying other object detection models and comparing results.

# Turn In
What to submit to ISVC:
- A link to the GitHub repository of your for this homework [private repo please] which should include your code and configuration files.   
- A publicly accessble http link to the location of your auto-uploaded objects in the cloud storage and a separate link(s) for maunally uploaded videos. 
- A document with problem statement and data collection approach (can be part of the repo as README file or a PDF) and a summary of your findings in this exercise (e.g. how good did the model do on your video? if it didn't do very good, can you hypothesize on the reasons for it - is it data quality issues, such as poor lighting conditions/low resolution/object occlusion, or was it poor performance of the model itself?)
