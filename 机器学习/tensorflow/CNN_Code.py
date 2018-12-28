# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""A very simple MNIST classifier.
See extensive documentation at
http://tensorflow.org/tutorials/mnist/beginners/index.md
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import data
from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string('data_dir', '/tmp/data/', 'Directory for storing data') # ��һ�������������ı����ϣ�����/tmp/data�ļ�����

print(FLAGS.data_dir)
mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1) # �����ĳ�ʼֵΪ�ض���̫�ֲ�
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
    """
    tf.nn.conv2d���ܣ�����4ά��input��filter�������һ��2ά�ľ�����
    ǰ���������ֱ���input, filter, strides, padding, use_cudnn_on_gpu, ...
    input   �ĸ�ʽҪ��Ϊһ��������[batch, in_height, in_width, in_channels],��������ͼ��߶ȣ�ͼ���ȣ�ͨ����
    filter  �ĸ�ʽΪ[filter_height, filter_width, in_channels, out_channels]���˲����߶ȣ���ȣ�����ͨ���������ͨ����
    strides һ����Ϊ4��list. ��ʾÿ�ξ���Ժ���input�л����ľ���
    padding ��SAME��VALID����ѡ���ʾ�Ƿ�Ҫ��������ȫ����Ĳ��֡������SAME������
    use_cudnn_on_gpu �Ƿ�ʹ��cudnn���١�Ĭ����True
    """
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    """
    tf.nn.max_pool �������ֵ�ػ�����,��avg_pool �����ƽ��ֵ�ػ�����
    ���������ֱ��ǣ�value, ksize, strides, padding,
    value:  һ��4D��������ʽΪ[batch, height, width, channels]����conv2d��input��ʽһ��
    ksize:  ��Ϊ4��list,��ʾ�ػ����ڵĳߴ�
    strides: ���ڵĻ���ֵ����conv2d�е�һ��
    padding: ��conv2d���÷�һ����
    """
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1], padding='SAME')

sess = tf.InteractiveSession()

x = tf.placeholder(tf.float32, [None, 784])
x_image = tf.reshape(x, [-1,28,28,1]) #�����밴�� conv2d��input�ĸ�ʽ��reshape��reshape

"""
# ��һ��
# �����(filter)�ĳߴ���5*5, ͨ����Ϊ1�����ͨ��Ϊ32����feature map ��ĿΪ32
# ����Ϊstrides=[1,1,1,1] ���Ե���ͨ��������ߴ�Ӧ�ø�����ͼ��һ�������ܵľ�����Ӧ��Ϊ?*28*28*32
# Ҳ���ǵ���ͨ�����Ϊ28*28������32��ͨ��,����?������
# �ڳػ��׶Σ�ksize=[1,2,2,1] ��ô�����������ػ��Ժ�Ľ������ߴ�Ӧ���ǣ�*14*14*32
"""
W_conv1 = weight_variable([5, 5, 1, 32])  # �������ÿ��5*5��patch�����32���������ֱ���patch��С������ͨ����Ŀ�����ͨ����Ŀ
b_conv1 = bias_variable([32])
h_conv1 = tf.nn.elu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

"""
# �ڶ���
# �����5*5������ͨ��Ϊ32�����ͨ��Ϊ64��
# ���ǰͼ��ĳߴ�Ϊ ?*14*14*32�� �����Ϊ?*14*14*64
# �ػ��������ͼ��ߴ�Ϊ?*7*7*64
"""
W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.elu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

# ������ �Ǹ�ȫ���Ӳ�,����ά��7*7*64, ���ά��Ϊ1024
W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.elu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
keep_prob = tf.placeholder(tf.float32) # ����ʹ����drop out,���������һЩcell���ֵΪ0�����Է�ֹ�����
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# ���Ĳ㣬����1024ά�����10ά��Ҳ���Ǿ����0~9����
W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])
y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2) # ʹ��softmax��Ϊ����༤���
y_ = tf.placeholder(tf.float32, [None, 10])

cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv), reduction_indices=[1])) # ��ʧ������������
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy) # ʹ��adam�Ż�
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1)) # ����׼ȷ��
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
sess.run(tf.initialize_all_variables()) # ������ʼ��
for i in range(20000):
    batch = mnist.train.next_batch(50)
    if i%100 == 0:
        # print(batch[1].shape)
        train_accuracy = accuracy.eval(feed_dict={
            x:batch[0], y_: batch[1], keep_prob: 1.0})
        print("step %d, training accuracy %g"%(i, train_accuracy))
    train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

print("test accuracy %g"%accuracy.eval(feed_dict={
    x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))
	
