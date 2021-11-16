# Labs 12.  NLP and Speech with Nvidia Nemo


These labs will focus on NLP and Speech tasks using the Nemo framework

### 0. Setting up the environment
Normally, Colab would be de rigeur here, but at the moment, Nemo Colab notebooks are broken.  Therefore, please provision a g4dn.2xlarge VM in AWS with the Nvidia Deep Learning AMI image.  Open port 8888.  Pull the container, e,g, ```docker pull nvcr.io/nvidia/nemo:1.4.0``` and then run it with jupyter inside, eg ```docker run --rm --gpus all --net=host -ti nvcr.io/nvidia/nemo:1.4.0 bash``` and then start jupyter lab inside the container, e.g. ```jupyter lab --allow-root --ip=0.0.0.0``` . Connect to the instance of jupyter in your browser.

While somewhat annoying, this approach is very flexible as you control the hardware you need as well as the exact version of the software

### 1. Introduction to Nemo
As you already learned in  async material, Nemo is a framework for ASR and NLP tasks.  Please review the list of [Nemo tutorials](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/starthere/tutorials.html). The tutorials will be found under the tutorials folder in your Jupyter Lab environment. Review the Nemo Primer.  Note, since we are running from a Nemo container, there is no need to reinstall Nemo (please ignore the corresponding cells in the notebooks)

### 2. Conversational AI Application
Run the Conversational AI application (/tutorials/AudioTranslationSample.ipynb) sample to see how to use Nemo for transcription. Try to load a different ASR model.. Does that work?

### 3. Voice Swap application
Try to voice swap application. Please explain how it works.

### 4. ASR with Nemo (/tutorials/asr/ASR_with_NeMo.ipynb)
We should now be ready to something more difficult. Run the 'ASR with Nemo' sample (sans the last, ONNX part). Notes:
* Can you load and use Tensorboard? Please open port 6006 in your VM
* Can you change the number of training epochs?
* Please take a look at your model config file.  Are you augmenting the dataset?
* Are you using pre-trained weights? If so, what are they?
* What is the sampling rate?
* Does the learning rate change help?
* When fine tuning QuartzNet, does it help to use mixed precision?
* On what dataset[s] was the pre-trained QuartzNet model originally trained?

### 5. (If there is time) - Voice commands with Nemo
Examine the Speech Command sample. What is the size of the dataset? How many parameters does the model have? how long does it take to fine tune?
