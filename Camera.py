import time
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera


class Camera:
    def __init__(self):
        self.camera = PiCamera()
        self.rawCapture = PiRGBArray(self.camera)

        # self.camera = cv2.VideoCapture(0)

        time.sleep(1.0)

    def read(self):
        self.camera.capture(self.rawCapture, format="bgr")
        return self.rawCapture.array

        # _, frame = self.camera.read()
        # return frame
