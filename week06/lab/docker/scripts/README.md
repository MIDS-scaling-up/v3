# Running from scripts

This is a very simple image classification example based on https://github.com/tensorflow/tensorrt/tree/master/tftrt/examples/image-classification updated to run on the Jetson devices. You'll learn how to use TensorFlow 2.x to convert a Keras model to three tf-trt models, a fp32, fp16, and int8. A simple set of test images will be used to both validate and benchmark both the native model and the three tf-trt ones.

This lab may require more memory than your device can provide.  As a workaround, you can run this script from the CLI without running a notebook.

If you wish to reduce the amount of memory your device is using, you can swith modes and disable the Desktop UI.  This can be done with the following command:

```
sudo init 3
```

To renable the desktop, you can either reboot or run the command:
```
sudo init 5
```

The basic TF-TRT conversion process looks like:

```
# max_workspace_size_bytes sets how much GPU memory will be avaible at runtime
# what happens if you make max value bigger (say 8000000000) or smaller (say 1000000000)?
max = 3000000000
conversion_params = trt.DEFAULT_TRT_CONVERSION_PARAMS._replace(
    precision_mode=trt.TrtPrecisionMode.FP16,
    max_workspace_size_bytes=max)
converter = trt.TrtGraphConverterV2(
   input_saved_model_dir='resnet50_saved_model', conversion_params=conversion_params)
converter.convert()
converter.save(output_saved_model_dir='resnet50_saved_model_TFTRT_FP16')
```

Based on your device, you may need to adjust the max_workspace_size_bytes.

See the TF-TRT documenation for additional options and details.


## Building the container (Optional)
If you wish to build the container locally, you'll need to run the command:
```
docker build -t tf-trt -f Dockerfile .
```
Note, this will take some time to complete.  Note, you'll need to update the container name used below to reference your local image.

## Start the container.
To start the container, select the following command based on your Jetson device.  
For NX devices:
```
docker run -ti --rm rdejana/tf-trt-demo:r32.6.1 bash
```

You'll be presenting with prompt similar to:
```
root@c65539299378:/app/tf-trt# 
```
You'll need to change to the directory `scripts`.
```
cd scripts
```

All the following commands will be executed from the scripts directory.

## Downloading the test images
The first step will be to download the test images; this is done with the command:
```
sh download.sh
```
This will download 4 images to new created data directory.
```
root@c65539299378:/app/tf-trt/scripts# ls -li data
total 916
27923312 -rw-r--r-- 1 root root  24112 Oct 16  2018 img0.JPG
27923313 -rw-r--r-- 1 root root 452718 Dec 14  2019 img1.JPG
27923315 -rw-r--r-- 1 root root 361413 Oct 30  2015 img2.JPG
27923316 -rw-r--r-- 1 root root  90994 Aug 13 18:51 img3.JPG
```

## Download and test a Keras model
The next step is to download the Keras ResNet50 model.  Run the command: 
```
python3 kerasModel.py
```
This will download the model, then run inference on it.  You'll see the someting like:
```
./data/img0.JPG - Predicted: [('n02110185', 'Siberian_husky', 0.55662125), ('n02109961', 'Eskimo_dog', 0.4173722), ('n02110063', 'malamute', 0.020951586)]
./data/img1.JPG - Predicted: [('n01820546', 'lorikeet', 0.30138993), ('n01537544', 'indigo_bunting', 0.16979575), ('n01828970', 'bee_eater', 0.16134118)]
./data/img2.JPG - Predicted: [('n02481823', 'chimpanzee', 0.5149864), ('n02480495', 'orangutan', 0.15896687), ('n02480855', 'gorilla', 0.15318167)]
./data/img3.JPG - Predicted: [('n01729977', 'green_snake', 0.43772438), ('n03627232', 'knot', 0.08848083), ('n01749939', 'green_mamba', 0.08080055)]
```
(grap the images and validate the results yourself!)

This program also converts the model to a saved model and makes sure it is still working.

```
saving model
WARNING:tensorflow:Compiled the loaded model, but the compiled metrics have yet to be built. `model.compile_metrics` will be empty until you train or evaluate the model.
2021-08-13 18:59:05.348362: W tensorflow/python/util/util.cc:348] Sets are not currently considered sequences, but this may change in the future, so consider avoiding using them.
/usr/local/lib/python3.6/dist-packages/tensorflow/python/keras/utils/generic_utils.py:497: CustomMaskWarning: Custom mask layers require a config and must override get_config. When loading, the custom mask layer must be passed to the custom_objects argument.
  category=CustomMaskWarning)
validating mdoel
WARNING:tensorflow:No training configuration found in save file, so the model was *not* compiled. Compile it manually.
./data/img0.JPG - Predicted: [('n02110185', 'Siberian_husky', 0.55662125), ('n02109961', 'Eskimo_dog', 0.4173722), ('n02110063', 'malamute', 0.020951586)]
```

If you are currious, the model is saved to the `models` directory.
```
root@c65539299378:/app/tf-trt/scripts# ls -li models/
total 4
56936 drwxr-xr-x 4 root root 4096 Aug 13 18:59 resnet50_saved_model
```

## Baseline the model
In this step, you'll get a baseline for how well the model performs.  Run the command
```
python3 benchmarkKeras.py 
```

Take note of how long 50 iterations take (on average) and how many images per second are processed.

## Convert to TF-TRT FP32
The next step is to apply the TF-TRT optimizations while using FP 32.  Run the command
```
python3 convertToTF_TRT_FP32.py 
```
When complete the model will be saved to the `models` directory.


## Benchmark the new model
You'll now benchmark your new model.  Run:
```
 python3 benchmarkTF_TRT_FP32.py 
```
Note, a prediction run is executed as part of the benchmark process; take note of the predictions for each image.

Once again, take note of how long 50 iterations take (on average) and how many images per second are processed.
How does it compare to the baseline?

## Convert to TF-TRT FP16
The next step is to apply the TF-TRT optimizations while using FP 32.  Run the command
```
python3 convertToTF_TRT_FP16.py 
```
When complete the model will be saved to the `models` directory.


## Benchmark the new FP16 model
You'll now benchmark your new FP16 model.  Run:
```
 python3 benchmarkTF_TRT_FP16.py 
```
Note, a prediction run is executed as part of the benchmark process; take note of the predictions for each image.

Once again, take note of how long 50 iterations take (on average) and how many images per second are processed.
How does it compare to the baseline and to the FP32 models?


## Convert to TF-TRT INT8 (NX only)
In this part of the lab, you'll move from floating point to integers and create an INT8 model.

Creating TF-TRT INT8 model requires a small calibration dataset. This data set ideally should represent the test data in production well, and will be used to create a value histogram for each layer in the neural network for effective 8-bit quantization.
For this lab, you'll use 4 images that you downloaded for calibration. In production, this set should be more representative of the production data.


```
python3 convertToTF_TRT_FP16.py 
```
When complete the model will be saved to the `models` directory.


## Benchmark the new INT8 model (NX only)
You'll now benchmark your new INT8 model.  Run:
```
 python3 benchmarkTF_TRT_INT8.py 
```
Once again, take note of how long 50 iterations take (on average) and how many images per second are processed.
How does it compare to the other models?  Is it worth the extra work?


Over all, what type of peformance improvements did you see? 

