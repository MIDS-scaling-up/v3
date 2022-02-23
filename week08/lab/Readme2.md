## Spring 2022 - Fun with EfficientDet

### Create and setup your env in AWS
1. Start AWS with nvidia deep learning ami (g4dn.2x.large) , open the port required for jupyter notebook. 
2. ssh to the AWS EC2 server 
3. Download the git repository :
` git clone https://github.com/zylo117/Yet-Another-EfficientDet-Pytorch.git`

3a. start a tmux session 

` tmux attach` 

4. start the nvidia pytorch container with enough shared memory : 

`docker run --rm -it --ipc=host -v ~/Yet-Another-EfficientDet-Pytorch:/Yet-Another-EfficientDet-Pytorch --gpus all --net=host nvcr.io/nvidia/pytorch:22.01-py3`


5. Once inside the container,  install the following software using the commands : 

`pip3 install jupyter lab
pip3 install numpy opencv-python tqdm tensorboard tensorboardX pyyaml webcolors matplotlib
apt-get update && apt-get install -y python3-opencv
`
### Run through the  logo example
* Open the jupyter lab / jupyter notebook and navigate to the tutorial folder and run the train_logo.ipynb . 
* Understand the notebook and read through every cell before executing.
* Observe the Average precision values. What are they? What do they mean? 

Note: `You may need to modify the first line in the notebook from !pip install pycocotools numpy==1.16.0 opencv-python tqdm tensorboard tensorboardX pyyaml webcolors matplotlib to !pip install pycocotools numpy opencv-python tqdm tensorboard tensorboardX pyyaml webcolors matplotlib`

### Modify the code to run on a different dataset
* Register on roboflow and download the public dataset (with coco label format) chess inside the docker container : 

`!curl -L <link from roboflow> > roboflow.zip; mkdir -p Yet-Another-EfficientDet-Pytorch/datasets/chess ; unzip roboflow.zip -d Yet-Another-EfficientDet-Pytorch/datasets/chess ; rm roboflow.zip

* Now please copy over the train_logo.ipynb to train_chess.ipynb in  the same folder and run the notebook after making necessary changes. 

* We need to create a folder called annotations inside the chess data directory and move the annotations to that folder .

* We also need to create projects/chess.yml . Everything can be the same as logo.yml except the project name and the obj_list. 
* The new obj_list for the chess dataset is : [ 'bishop', 'black-bishop', 'black-king', 'black-knight',  'black-pawn', 'black-queen', 'black-rook', 'white-bishop', 'white-king',  'white-knight', 'white-pawn', 'white-queen',  'white-rook' ] >



* After running the notebook, observe the Average precision values. Is it better or worse than in the logo notebook. What does this tell us ?

### Get the code to run on the Jetson device
* Download the appropriate pytorch container from nvidia.  

* Clone the git repository 
`git clone https://github.com/zylo117/Yet-Another-EfficientDet-Pytorch.git`

* Copy over the notebook train_chess_jetson.ipynb and the file coco_eval.py to the appropriate directories. 
* Start the docker container
* Once inside the docker container : run the jupyter notebook
* Download the best model from the cloud into the corresponding directories in the Jetson
* Run the inference

