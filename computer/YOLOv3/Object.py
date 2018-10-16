from pydarknet import Detector, Image
import cv2
import os


class Object_Detection():
    def __init__(self):
        self.net = Detector(bytes("cfg/yolo-obj.cfg", encoding="utf-8"), bytes("cfg/yolo-obj_400.weights", encoding="utf-8"), 0, bytes("cfg/obj.data", encoding="utf-8"))

    def Detection(self, img):
        img2 = Image(img)
        results = self.net.detect(img2)
        # print(results)
        # print(results)
        for cat, score, bounds in results:
            x, y, w, h = bounds
            cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0),
                          thickness=2)
            cv2.putText(img, str(cat.decode("utf-8")), (int(x - w / 2 - 1), int(y - h / 2 - 1)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))
            print(cat)
        return img
#	return results



