from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib

from EyeDetector import EyeDetector
from Camera import Camera

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

    # 1초 동안 실행 정지
    time.sleep(1.0)

    temp_count = 0
    total_blink_count = 0

    # 무한 반복문으로 비디오의 프레임 하나씩 각각 처리
    while True:
        frame = camera.read()
        probability = detector.update(frame)

        if probability is not None:
            # 눈이 떠져있을 확률이 20% 보다 낮아지면,
            # 눈을 감고 있는 것으로 인식하고 임시 카운트 증가
            if probability < 0.2:
                temp_count += 1

            # 눈의 크기가 설정해놓은 경계보다 클 때 (눈을 떴을 때)
            else:
                # 만약 일정 프레임 이상 눈을 감고 있었으면 눈 깜빡임 카운트 증가
                if temp_count >= blink_consec_frames:
                    total_blink_count += 1
                    print("***************************** Blink! " +
                          str(total_blink_count))

                # 임시 카운트 리셋
                temp_count = 0

            # 화면에 눈의 크기 표시
            # cv2.putText(frame, "Blink: {}".format(total_blink_count), (10, 30),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            # cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # 두 눈 각각을 나타내는 좌표들을 이어서 초록색 선을 그림
            # left_eye_hull = cv2.convexHull(left_eye)
            # right_eye_hull = cv2.convexHull(right_eye)
            # cv2.drawContours(frame, [left_eye_hull], -1, (0, 255, 0), 1)
            # cv2.drawContours(frame, [right_eye_hull], -1, (0, 255, 0), 1)

        # 현재 프레임 보여줌
        # cv2.imshow("Frame", frame)

        # key = cv2.waitKey(1) & 0xFF

        # q 눌리면 프로그램 종료
        # if key == ord("q"):
        #     break

    # 띄운 윈도우와 비디오 스트리밍 종료
    camera.release()


if __name__ == "__main__":
    main()
