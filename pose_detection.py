import cv2 as cv
import mediapipe as mp
import time

class Pose_detector:
    def __init__(self,mode = False, upper_body = False, smooth_landmark = True, min_detection_confidence = 0.5,  tracking_confidence = 0.5):
        self.mode = mode
        self.upper_body = upper_body
        self.smooth_landmark = smooth_landmark
        self.min_detection_confidence = min_detection_confidence
        self.tracking_confidence = tracking_confidence
        
        self.mypose = mp.solutions.pose
        self.mpDraw = mp.solutions.drawing_utils
        self.pose = self.mypose.Pose()
        
    def findpose(self, img, draw=True):
        if img is None:
            return
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks and draw:
            self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mypose.POSE_CONNECTIONS)
        return img
    
    def getPosition(self,img,draw=True):
        lmlist = []
        if self.results.pose_landmarks and draw:
            for id,lm in enumerate(self.results.pose_landmarks.landmark):
                h , w , c = img.shape
                cx , cy = int(lm.x * w) , int(lm.y * h)
                lmlist.append([id,cx,cy])
                cv.circle(img,(cx,cy),10,(225,225,225),4)
                
        return lmlist
    
if __name__ == "__main__":
    main()