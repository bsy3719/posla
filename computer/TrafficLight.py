#!/usr/bin/python

from __future__ import print_function

import cv2 as cv
import numpy as np


#img is must be traffic light object image
def circle(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.medianBlur(gray, 5)
    src = img.copy()
    state = ''
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 10, np.array([]), 100, 30, 60, 60)
    if circles is not None:
        a, b, c = circles.shape
        if b > 2:
            for i in range(b):
                # print(circles)
                cv.circle(src, (circles[0][i][0], circles[0][i][1]), circles[0][i][2], (0, 0, 255), 3, cv.LINE_AA)
                # print(i, "circles BGR is = ", img[int(circles[0][i][1]), int(circles[0][i][0])])
                if i == 2 and img[int(circles[0][i][1]), int(circles[0][i][0])][2] > 200:
                    state = "red"
                elif i == 1 and img[int(circles[0][i][1]), int(circles[0][i][0])][1] > 200:
                    state = "green"
                elif i == 1 and img[int(circles[0][i][1]), int(circles[0][i][0])][1] > 170 and \
                    img[int(circles[0][i][1]), int(circles[0][i][0])][2] > 200:
                    state = "yellow"
    return state, src
# def angle(dx, dy):
#     return math.atan2(dy, dx) * 180 / math.pi
#
# def line(pic):
#     row, col, ch = pic.shape
#     a, b, c = lines.shape
#     (d, e) = (row / 2, col / 2)
#     (f, g) = (-1, -1)
#     for i in range(a):
#         (x1, y1, x2, y2) = (lines[i][0][0], lines[i][0][1], lines[i][0][2], lines[i][0][3])
#         if max(y1, y2) > row / 2 and min(x1, x2) < col/2 and angle(x2 - x1, y2 - y1) < 0:
#             d = max(y1, y2)
#             f = i
#         if max(y1, y2) > row / 2 and min(x1, x2) > col/2 and angle(x2 - x1, y2 - y1) > 0:
#             e = max(y1, y2)
#             g = i
#
#
#     if f is not -1:
#         (x1, y1, x2, y2) = (lines[f][0][0], lines[f][0][1], lines[f][0][2], lines[f][0][3])
#         print("left side angle is", angle(x2 - x1, y2 - y1))
#         cv.line(src, (x1, y1), (x2, y2), (0, 0, 255), 3, cv.LINE_AA)
#     if g is not -1:
#         (x1, y1, x2, y2) = (lines[g][0][0], lines[g][0][1], lines[g][0][2], lines[g][0][3])
#         print("right side angle is", angle(x2 - x1, y2 - y1))
#         cv.line(src, (x1, y1), (x2, y2), (0, 0, 255), 3, cv.LINE_AA)

