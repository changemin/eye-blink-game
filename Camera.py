import time

raspiMode = False

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    isRaspi = True
except ImportError:
    import cv2


class Camera:
    def __init__(self):
        self.camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        # self.camera = cv2.VideoCapture(0)
        # time.sleep(1.0)

    def read(self):
    
        _, frame = self.camera.read()
        return frame

    def release(self):
        print("releasing...")
