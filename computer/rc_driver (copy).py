__author__ = 'zhengwang'

import socket
import time
import os

import sys
import threading
import socketserver
import numpy as np
import socket
import cv2

from model import NeuralNetwork
# from rc_driver_helper import *


class CollectTrainingData(object):

    def __init__(self, host, port, input_size):

        # self.server_socket = socket.socket()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)

        # accept a single connection
        # self.connection = self.server_socket.accept()[0].makefile('rb')
        self.connection = self.server_socket.accept()[0]
        self.send_inst = True

        self.input_size = input_size

        # model create
        model = NeuralNetwork()
        model.load_model(path = './model_data/VGG_model.h5')

    def collect(self):

        # collect images for training
        print("Start collecting images...")
        print("Press 'q' or 'x' to finish...")
        start = cv2.getTickCount()

        X = np.empty((0, self.input_size))
        y = np.empty((0, 4))

        # stream video frames one by one
        try:
            stream_bytes = b' '
            frame = 1
            cnt = 0
            while self.send_inst:
                # stream_bytes += self.connection.read(1024)
                stream_bytes += self.connection.recv(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')

                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]

                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                    #rgb = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    # select lower half of the image
                    height, width = image.shape
                    # roi = image[int(height/2):height, :]
                    roi = image[120:240, :]

                    #cv2.imshow('roi', roi)
                    cv2.imshow('origin', image)

                    # reshape the roi image into a vector
                    image_array = roi.reshape(1, int(height / 2) * width).astype(np.float32)

                    # # neural network makes prediction
                    # prediction = self.model.predict(image_array)
                    #
                    # if prediction == 2:
                    #     self.connection.send('w'.encode())
                    #     print("Forward")
                    # elif prediction == 0:
                    #     self.connection.send('a'.encode())
                    #     print("Left")
                    # elif prediction == 1:
                    #     self.connection.send('c'.encode())
                    #     print("Right")
                    # else:
                    #     self.stop()

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            end = cv2.getTickCount()
            # calculate streaming duration
            print("Streaming duration: , %.2fs" % ((end - start) / cv2.getTickFrequency()))

        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == '__main__':
    # host, port
    h, p = "192.168.0.90", 5034
    # vector size, half of the image
    s = 120 * 320

    ctd = CollectTrainingData(h, p, s)
    ctd.collect()