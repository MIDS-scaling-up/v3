# convert to FP16

from __future__ import absolute_import, division, print_function, unicode_literals
import os
import time

import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from tensorflow.python.compiler.tensorrt import trt_convert as trt
from tensorflow.python.saved_model import tag_constants
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

print('Converting to TF-TRT FP16...')

# max_workspace_size_bytes sets how much GPU memory will be avaible at runtime
# what happens if you make max value bigger (say 8000000000) or smaller (say 1000000000)?
max = 3000000000
conversion_params = trt.DEFAULT_TRT_CONVERSION_PARAMS._replace(
    precision_mode=trt.TrtPrecisionMode.FP16,
    max_workspace_size_bytes=max)
converter = trt.TrtGraphConverterV2(
   input_saved_model_dir='models/resnet50_saved_model', conversion_params=conversion_params)
converter.convert()
converter.save(output_saved_model_dir='models/resnet50_saved_model_TFTRT_FP16')
print('Done Converting to TF-TRT FP16')

