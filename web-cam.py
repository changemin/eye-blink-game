import cv2, time

video = cv2.VideoCapture(1, cv2.CAP_DSHOW)

check, frame = video.read()

print(check)
print(frame)

cv2.imshow("capture", frame)

cv2.waitKey(0)
video.release()
cv2.destroyAllWindows()