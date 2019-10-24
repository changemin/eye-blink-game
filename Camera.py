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
        if raspiMode:
            self.camera = PiCamera()
            self.camera.resolution = (640, 480)
            self.camera.framerate = 32
            self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        else:
            self.camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        time.sleep(1.0)

    def read(self):
        if raspiMode:
            self.camera.capture(self.rawCapture, format="bgr")
            self.rawCapture.truncate(0)
            return self.rawCapture.array
        else:
            _, frame = self.camera.read()
            return frame

    def release(self):
        print("releasing...")
        if raspiMode:
            self.camera.release()
