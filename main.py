from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import random

from EyeDetector import EyeDetector
from Camera import Camera

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    isRaspi = True
except ImportError:
    import cv2

WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 1920

raspiMode = False
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", default="./data/shape_predictor_68_face_landmarks.dat",
                help="path to facial landmark predictor")
ap.add_argument("-f", "--frames", type=int, default=2,
                help="the number of consecutive frames the eye must be below the threshold")

args = vars(ap.parse_args())


def main():
    detector = EyeDetector(args["shape_predictor"])
    blink_consec_frames = args["frames"]
    camera = Camera()

    temp_count = 0
    total_blink_count = 0

    # 무한 반복문으로 비디오의 프레임 하나씩 각각 처리
    while True:
        frame = camera.read()
        left_eye_rect, right_eye_rect, probability = detector.update(frame)

        if probability is not None:
            # 눈이 떠져있을 확률이 20% 보다 낮아지면,
            # 눈을 감고 있는 것으로 인식하고 임시 카운트 증가
            if probability < 0.5:
                temp_count += 1

            # 눈의 크기가 설정해놓은 경계보다 클 때 (눈을 떴을 때)
            else:
                # 만약 일정 프레임 이상 눈을 감고 있었으면 눈 깜빡임 카운트 증가
                if temp_count >= blink_consec_frames:
                    total_blink_count += 1
                    print("*************Blink! " +
                          str(total_blink_count))

                # 임시 카운트 리셋
                temp_count = 0

            if not raspiMode:
                # 화면에 눈의 크기 표시
                cv2.putText(frame, "Score: {}".format(total_blink_count*100), (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame, "percent: {:.2f}".format(probability[0][0]), (300, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                cv2.rectangle(frame, (left_eye_rect[0], left_eye_rect[1]), (
                    left_eye_rect[2], left_eye_rect[3]), (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)), 3)
                cv2.rectangle(frame, (right_eye_rect[0], right_eye_rect[1]), (
                    right_eye_rect[2], right_eye_rect[3]), (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)), 3)

        if not raspiMode:
            # 현재 프레임 보여줌
            # cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)
            # cv2.setWindowProperty("Frame",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
            dst = cv2.resize(frame, dsize=(WINDOW_WIDTH, WINDOW_WIDTH), interpolation=cv2.INTER_AREA)
            cv2.imshow("Frame",dst)

            key = cv2.waitKey(1) & 0xFF

            # q 눌리면 프로그램 종료
            if key == ord("q"):
                # 띄운 윈도우와 비디오 스트리밍 종료
                camera.release()
                cv2.destroyAllWindows()
                break


if __name__ == "__main__":
    main()
