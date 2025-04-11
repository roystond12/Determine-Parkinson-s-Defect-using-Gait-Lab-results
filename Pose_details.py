import mediapipe.python.solutions as solutions
import pose_detection as pose
import cv2 as cv
import mediapipe as mp
import time

def step_length(list1,list2):
    x1,y1 = list1[1:]
    x2,y2 = list2[1:]
    distance = ((y2 - y1)**2 + (x2 - x1)**2)**0.5
    return distance
def stride_width(stride1, stride2, stride3, stride4):
    x1, y1 = stride1[1:]
    x2, y2 = stride2[1:]
    x3, y3 = stride3[1:]
    x4, y4 = stride4[1:]
    distance1 = ((y4 - y1)**2 + (x4 - x1)**2)**0.5
    distance2 = ((y3 - y2)**2 + (x3 - x2)**2)**0.5
    return min(distance1, distance2)

cap = cv.VideoCapture(0)
detector = pose.Pose_detector()
step_length1 = []
step_length_min1 = 10000
step_length_min2 = 10000
step_length2 = []
stride1 = stride2 = stride3 = stride4 = None

while True:
    success, img = cap.read()
    img = detector.findpose(img)
    list = detector.getPosition(img)
    if list:
        if list[29][2] < step_length_min1 and list[30][2] < step_length_min2:
            step_length1 = list[29]
            step_length_min1 = list[29][2]
            step_length2 = list[30]
            step_length_min2 = list[30][2]
            stride1 = list[29]
            stride2 = list[30]
            stride3 = list[31]
            stride4 = list[32]

    cv.imshow("Image", img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

if stride1 and stride2 and stride3 and stride4:
    stride_w = stride_width(stride1, stride2, stride3, stride4)
    print("Stride Width:", stride_w)
else:
    print("Stride data not available")

cap.release()
cv.destroyAllWindows()

cap.release()
cv.destroyAllWindows()

