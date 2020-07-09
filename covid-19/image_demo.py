#! /usr/bin/env python
# coding=utf-8
#================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : VIM
#   File name   : image_demo.py
#   Author      : YunYang1994
#   Created date: 2019-01-20 16:06:06
#   Description :
#
#================================================================

import cv2
import numpy as np
import core.utils as utils
import tensorflow as tf
from core.config import cfg
from PIL import Image

return_elements = ["input/input_data:0", "pred_sbbox/concat_2:0", "pred_mbbox/concat_2:0", "pred_lbbox/concat_2:0"]
pb_file         = "./yolov3_voc.pb"
save_path       = "./docs/output/res.txt"
image_path      = "./docs/images/"
num_classes     = 2
input_size      = 416
graph           = tf.Graph()

tf.app.flags.DEFINE_string('image_name', '2020.02.10.20021584-p6-52%11.png', 'input image')
FLAGS = tf.app.flags.FLAGS
original_image = cv2.imread(image_path+FLAGS.image_name)
original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
original_image_size = original_image.shape[:2]
image_data = utils.image_preporcess(np.copy(original_image), [input_size, input_size])
image_data = image_data[np.newaxis, ...]

return_tensors = utils.read_pb_return_tensors(graph, pb_file, return_elements)


with tf.Session(graph=graph) as sess:
    pred_sbbox, pred_mbbox, pred_lbbox = sess.run(
        [return_tensors[1], return_tensors[2], return_tensors[3]],
                feed_dict={ return_tensors[0]: image_data})

pred_bbox = np.concatenate([np.reshape(pred_sbbox, (-1, 5 + num_classes)),
                            np.reshape(pred_mbbox, (-1, 5 + num_classes)),
                            np.reshape(pred_lbbox, (-1, 5 + num_classes))], axis=0)

bboxes = utils.postprocess_boxes(pred_bbox, original_image_size, input_size, 0.3)
bboxes = utils.nms(bboxes, 0.45, method='nms')
#因为每图只有一个框所以直接返回box的预测值0617
classes=utils.read_class_names(cfg.YOLO.CLASSES)
for i,bbox in enumerate(bboxes):
    file = open('./docs/output/out.txt', 'w+')
    file.write(classes[int(bbox[5])])
    file.write('\n')
    file.write(str(bbox[4]))
    #print(classes[int(bbox[5])])
file.close()
image = utils.draw_bbox(original_image, bboxes)
image = Image.fromarray(image)
image.save("./docs/output/%s" % (FLAGS.image_name))
#image.show()





