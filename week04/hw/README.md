#### Homework 4: DL 101

You will run this homework in colab, and build your own MLP architecture.   
Provided with the homework is a dataset and the pipeline to process the data and load to GPU. Please make sure you are comfortable with the preprocessing of the data.  
We also provide a logistic regression model implemented in pytorch, along with a benchmarked AUC score.  
  
Your task will be to build an Multi layer perceptron, or MLP, and improve on the score achieved by the LR model.  
Try things like,  
-  Adding multiple hidden layers (you can reference [this](https://www.kaggle.com/lopuhin/mercari-golf-0-3875-cv-in-75-loc-1900-s) prize winning architecture for an initial set of layer dimensions).  
-  As you introduce more parameters, you will probaby need to drop the learning rate to avoid overfitting.  
-  Does [dropout](https://pytorch.org/docs/stable/generated/torch.nn.Dropout.html) help to avoid overfitting.  
-  Add a [relu](https://pytorch.org/docs/master/generated/torch.nn.functional.relu.html#torch.nn.functional.relu) activation between hidden layers.  
-  Experiment with increasing or decreasing batch size. Or a good way to regularise is starting with small batchsizes and increasing batchsize each epoch.  
-  Add a small weight decay to your [Adam optimiser](https://pytorch.org/docs/stable/optim.html).   
After you are happy with the results, download the notebook as a html and submit it to ISVC, together with the highest AUC score you achieved.  
  
You can get started [here](https://colab.research.google.com/drive/1kqbgfc1Lv3DXP6EdbpfQtMCsTHFR3wHA?usp=sharing).  