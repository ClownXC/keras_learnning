#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project: vegetables_classify
@File: index.py
@Description: //todo
@Author: chen
@Email: chen3494269@163.com
@Date: 2022/3/17 13:24
"""
import json

import keras.models
from flask import Flask, request
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['simhei']
plt.rcParams['axes.unicode_minus'] = False
from PIL import Image

app = Flask(__name__)
MODEL_PATH = "./vegetable_model_v1.h5"
model = keras.models.load_model(MODEL_PATH)
IMAGE_SIZE = (160, 160)
CLASS_NAMES = ['玉米', '茄子', '萝卜']
SUCCESS = 0
FAILURE = -1


def success(data):
    """
    成功返回
    @param data:
    @return:
    """
    res = {
        'code': SUCCESS,
        'msg': '识别成功',
        'data': data
    }
    return json.dumps(res, ensure_ascii=False)


def failure(msg=None):
    """
    @param msg:
    @return:
    """
    res = {
        'code': FAILURE,
        'msg': '识别失败' if not msg else msg
    }
    return json.dumps(res, ensure_ascii=False)


@app.route("/analyzer", methods=["POST"])
def analyzer():
    """
    @return:
    """
    file = request.files.get("file")
    if file:
        try:
            test_images_src = Image.open(file)
            test_images_src = test_images_src.resize(IMAGE_SIZE, Image.ANTIALIAS)
            test_images_arr = image.img_to_array(test_images_src)
            test_image = tf.expand_dims(test_images_arr, axis=0)
            predictions = model.predict_on_batch(test_image)
            class_name = CLASS_NAMES[np.argmax(predictions[0])]
            return success({
                'class_name': class_name
            }), 200
        except Exception:
            return failure({

            }), 500
    else:
        return "file not found", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
