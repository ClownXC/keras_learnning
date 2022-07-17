#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project: vegetables_classify
@File: train.py
@Description: //todo
@Author: chen
@Email: chen3494269@163.com
@Date: 2022/3/17 09:34
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf

from pathlib import Path

from tensorflow.keras.preprocessing import image_dataset_from_directory
import matplotlib.pyplot as plt
import numpy as np
import tensorflow.keras as keras

plt.rcParams['font.sans-serif'] = ['simhei']
plt.rcParams['axes.unicode_minus'] = False

PATH = Path("/chen/data_edgeai-app")
train_dir = PATH / "train"
validation_dir = PATH / "validation"
MODEL_PATH = "./vegetable_model_v1.h5"

IMAGE_SIZE = (160, 160)
BATCH_SIZE = 32

train_dataset = image_dataset_from_directory(
    train_dir,
    label_mode="categorical",
    shuffle=True,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)

validation_dataset = image_dataset_from_directory(
    train_dir,
    label_mode="categorical",
    shuffle=True,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)

val_batches = tf.data.experimental.cardinality(validation_dataset)
test_dataset = validation_dataset.take(val_batches // 6)
validation_dataset = validation_dataset.skip(val_batches // 6)

class_names = train_dataset.class_names

# 提前加载数据, 防止 IO 阻塞
AUTOTUNE = tf.data.AUTOTUNE
# 数据加载优化
train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)
test_dataset = test_dataset.prefetch(buffer_size=AUTOTUNE)

plt.figure(figsize=(10, 10))
for images, labels in train_dataset.take(1):
    for i in range(9):
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(images[i].numpy().astype("uint8"))
        plt.title(class_names[np.argmax(labels[i])])
        plt.axis("off")
plt.show()
plt.close("off")

data_augmentation = keras.Sequential([
    keras.layers.experimental.preprocessing.RandomFlip("horizontal"),
    keras.layers.experimental.preprocessing.RandomRotation(0, 2)
])

x = keras.Input(160, 160, 3)
# 图像像素缩放到[-1, 1]
preprocess_input = keras.applications.mobilenet_v2.preprocess_input
global_average_layer = keras.layers.GlobalAveragePooling2D()

IMG_SHAPE = IMAGE_SIZE + (3,)
base_model = keras.applications.MobileNetV2(
    input_shape=IMG_SHAPE,
    include_top=False,
    weights="imagenet"
)

# 冻结卷积基
base_model.trainable = False

# 分类层
prediction_layer = keras.layers.Dense(len(class_names), activation="softmax")

# 特征提取
inputs = keras.Input(IMG_SHAPE)
x = data_augmentation(x)
x = preprocess_input(x)
x = base_model(x, training=False)
x = global_average_layer(x)
x = keras.layers.Dropout(0.2)(x)
outputs = prediction_layer(x)

# 模型训练
base_learning_rate = 0.0001
model = keras.Model(inputs, outputs)
model.compile(optimizer=keras.optimizers.Adam(lr=base_learning_rate),
              loss=keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

initial_epochs = 1
model.fit(
    train_dataset,
    epochs=initial_epochs,
    validation_data=validation_dataset
)

loss, accuracy = model.evaluate(test_dataset)
print("Test accuracy: ", accuracy)

model.save(MODEL_PATH)
