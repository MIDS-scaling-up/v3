## Week 13 labs

### Triton Inference Server primer
Triton Inference server is designed to help you create services out of your trained models.  In this lab, we will follow the [Triton IS QuickStart](https://github.com/triton-inference-server/server/blob/main/docs/quickstart.md). A few quick notes:
* First, provision a g4dn.2xlarge virtual machine in AWS. Use the Nvidia Deep Learning AMI
* Go to your home diretory and clone the Triton IS server repo, e.g. ```https://github.com/triton-inference-server/server.git```
* The current tag is 21.11, so the pull commands are:
```
docker pull nvcr.io/nvidia/tritonserver:21.11-py3-sdk (client)
docker pull nvcr.io/nvidia/tritonserver:21.11-py3 (server)
```
A few quick questions:
* is your server using the GPU?
* Can you change the number of classes for scoring in the example?
* Which model is being used for inference? Can you change it to a different model?
* Can you get the metrics for your server?

### RAPIDS primer


2. NVTabular / Huge CTR


