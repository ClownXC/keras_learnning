#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project: vegetables_classify
@File: predict.py
@Description: //todo
@Author: chen
@Email: chen3494269@163.com
@Date: 2022/3/17 10:24
"""

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow.keras.preprocessing import image
import requests
import tensorflow.keras as keras
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['simhei']
plt.rcParams['axes.unicode_minus'] = False


MODEL_PATH = "./vegetable_model_v1.h5"
TMP_IMAGE_PATH = './tmp.png'
IMAGE_SIZE = (160, 160)
CLASS_NAMES = ['玉米', '茄子', '萝卜']


def get_image(img_url):
    """
    @param img_url:
    @return:
    """
    res = requests.get(img_url, stream=True)
    if res.status_code == 200:
        with open(TMP_IMAGE_PATH, "wb") as f:
            f.write(res.content)
            print("success")
        return TMP_IMAGE_PATH
    else:
        return None


# 预测
def predict():
    test_images_src = image.load_img(TMP_IMAGE_PATH, target_size=IMAGE_SIZE)
    test_images_arr = image.img_to_array(test_images_src)
    test_image = tf.expand_dims(test_images_arr, axis=0)
    model = keras.models.load_model(MODEL_PATH)
    predictions = model.predict_on_batch(test_image)

    plt.imshow(test_images_arr.astype("uint8"))
    plt.title(CLASS_NAMES[np.argmax(predictions[0])])
    plt.axis("off")
    plt.show()
    plt.close("all")


if __name__ == '__main__':
    image_url = ''
    if get_image(image_url):
        predict()
