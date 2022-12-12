# Homework 6

## Model optimization and quantization

In lab, you saw to how use leverage TensorRT with TensorFlow.  For this homework, you'll look at Hugging Face 🤗 Optimum (https://huggingface.co/docs/optimum/main/en/index). Go over training materials provided in the documentation.

You first need to train a custom image classification model, using either the fruit example or your own set of classes. Like in the lab, you'll want to first baseline the your model, looking a the number of images per second it can process.  You may train the model on a GPU eanabled server/virtual machine.  Once you have your baseline, follow the steps/examples from Hugging Face 🤗 Optimum to optimize and quantize the model. 

You may use either the container apporach or build the library from source.

## Turn-in
You'll need to submit:
- The base model you used
- A description of your data set
- How long you trained your model, how many epochs you specified, and the batch size.
- Native Pytorch baseline
- Optimized performance numbers
- Code used for optimization

