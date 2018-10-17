#!/usr/bin/python


# Python 2/3 compatibility
from __future__ import print_function

import cv2
import numpy as np
import math
import queue

class Stop():
    def __init__(self):
        self.sum_cx1 = self.sum_cy1 = self.sum_cx2 = self.sum_cy2 = 0
        self.filtercnt = 100
        self.MAF = queue.Queue()

    def angle(self, dx, dy):
        return math.atan2(dy, dx) * 180 / math.pi

    def push(self, x1, y1, x2, y2):
        self.MAF.put((x1, y1, x2, y2))
        self.sum_cx1 += x1
        self.sum_cy1 += y1
        self.sum_cx2 += x2
        self.sum_cx2 += y2

    def pop(self):
        (x1, y1, x2, y2) = self.MAF.get()
        self.sum_cx1 -= x1
        self.sum_cy1 -= y1
        self.sum_cx2 -= x2
        self.sum_cx2 -= y2

    def GetStopLine(self, img):
        edge = cv2.Canny(img, 200, 350)
        row, col, ch = img.shape
        # print(img.shape)
        lines = cv2.HoughLinesP(edge, 1, math.pi / 180.0, 50, np.array([]), 50, 80)
        cx1 = cy1 = cx2 = cy2 = 0
        if lines is not None:
            a, b, c = lines.shape
            (d, e) = (row / 2, col / 2)
            (f, g) = (-1, -1)

            cnt = 0
            for i in range(a):
                # print(i)
                (x1, y1, x2, y2) = (lines[i][0][0], lines[i][0][1], lines[i][0][2], lines[i][0][3])
                #Average Stop Line cordinate in this frame
                if x1 < col / 2 and x2 > col / 2 and abs(self.angle(x2 - x1, y2 - y1)) < 5:
                    cx1 += x1
                    cx2 += x2
                    cy1 += y1
                    cy2 += y2
                    cnt += 1

            if cnt is not 0:
                (cx1, cy1, cx2, cy2) = (int(cx1 / cnt), int(cy1 / cnt), int(cx2 / cnt), int(cy2 / cnt))
                print((cx1, cy1, cx2, cy2))
        #Moving Average Filter for Stop Line Calibration
        if self.MAF.qsize() <= self.filtercnt:
            self.push(cx1, cy1, cx2, cy2)
        if self.MAF.qsize() > self.filtercnt:
            self.pop()
        if self.MAF.qsize() == self.filtercnt:
            (cx1, cy1, cx2, cy2) = (self.sum_cx1 / self.filtercnt, self.sum_cy1 / self.filtercnt, self.sum_cx2 / self.filtercnt, self.sum_cy2 / self.filtercnt)
        # cv2.line(img, (int(cx1), int(cy1)), (int(cx2), int(cy2)), (0, 0, 255), 3, cv2.LINE_AA)
        # print("Detected Stop Line's angle is", angle(cx2 - cx1, cy2 - cy1))
        cv2.imshow('Detected Line', img)
        if cx1 is not 0 and cy1 is not 0 and cx2 is not 0 and cy2 is not 0:
            return True
        else:
            return False

# def main():
#     cap = cv2.VideoCapture(0)
#     while True:
#         _, origin = cap.read()
#         resize_img = cv2.resize(origin, dst=None, dsize=(320, 240), interpolation=cv2.INTER_CUBIC)
#         roi = resize_img[120:, :]
#         roi_edge = cv2.Canny(roi, 200, 300)
#         Line = Stop()
#         test_img = Line.GetStopLine(roi)
#         cv2.imshow('origin', resize_img)
#         print(test_img)
#         cv2.imshow('edge', roi_edge)
#         ch = cv2.waitKey(1)
#         if ch == 27:
#             break
#     cv2.destroyAllWindows()
#
# main()
