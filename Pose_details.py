import mediapipe.python.solutions as solutions
import pose_detection as pose
import cv2 as cv
import mediapipe as mp
import time
from flask import Blueprint, render_template,jsonify,request
import pickle
import numpy as np
import os


def swap_foot_indices(landmarks):
    swapped = landmarks.copy()
    swapped[31], swapped[32] = landmarks[32], landmarks[31]
    return swapped


def euclidean_distance(p1, p2):
    return np.linalg.norm(np.array([p1[0], p1[1]]) - np.array([p2[0], p2[1]]))


def get_reference_height(landmarks):
    left_ankle = landmarks[27]
    right_ankle = landmarks[28]
    ankle_midpoint = [(left_ankle[0] + right_ankle[0])/2, (left_ankle[1] + right_ankle[1])/2]
    return euclidean_distance(landmarks[0], ankle_midpoint) + 1e-6 


def get_step_length_mean(landmarks):
    left_foot = landmarks[31] 
    right_foot = landmarks[32] 
    ref_height = get_reference_height(landmarks)    
    step_length = euclidean_distance(left_foot, right_foot)
    return step_length / ref_height


def get_velocity(landmark_series, frame_rate=30):
    total_distance = 0
    ref_height = get_reference_height(landmark_series[0])   
    for i in range(1, len(landmark_series)):
        left = landmark_series[i][27]
        prev_left = landmark_series[i-1][27]
        total_distance += euclidean_distance(left, prev_left)
    total_time = len(landmark_series) / frame_rate
    return (total_distance / total_time) / ref_height if total_time > 0 else 0


def get_cadence(ankle_y_series, frame_rate=30):
    steps = 0
    threshold = 0.02
    for i in range(1, len(ankle_y_series) - 1):
        if ankle_y_series[i-1] > ankle_y_series[i] < ankle_y_series[i+1] and (ankle_y_series[i-1] - ankle_y_series[i]) > threshold:
            steps += 1
    total_time = len(ankle_y_series) / frame_rate
    return (steps / total_time) * 60 if total_time > 0 else 0


def get_ambulation_time(frame_count, frame_rate=30):
    return frame_count / frame_rate


def get_egvi_variance(foot_landmark_series):
    ref_height = get_reference_height(foot_landmark_series[0])
    step_lengths = []
    for i in range(1, len(foot_landmark_series)):
        step_lengths.append(
            euclidean_distance(foot_landmark_series[i][31], foot_landmark_series[i-1][31])
        )
    return np.std(step_lengths) / ref_height


def get_mean_egvi(left_egvi, right_egvi):
    return (left_egvi + right_egvi) / 2


pose_details = Blueprint("pose_details",__name__,static_folder="static",template_folder="templates")
with open('parkinson_model.pkl', 'rb') as file:
    model = pickle.load(file)


UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
pose_details.root_path = UPLOAD_FOLDER


@pose_details.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return "No file part"
        
    file = request.files['video']
    if file.filename == '':
        return "No selected file"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    cap = cv.VideoCapture(filepath)

    detector = pose.Pose_detector()
    step_length1 = []
    step_length_min1 = 10000
    step_length_min2 = 10000
    step_length2 = []
    stride1 = stride2 = stride3 = stride4 = None
    step_means = []
    velocities = []
    cadences = []
    amb_times = []
    left_egvis = []
    right_egvis = []

    while True:
        success, img = cap.read()
        if img is None:
            break
        img = detector.findpose(img)
        list = detector.getPosition(img)
        if list:
            step_means.append(get_step_length_mean(list))
            velocities.append(get_velocity([list]))         # pass history to get velocity
            cadences.append(get_cadence([list[27][1]]))      # from ankle Y positions
            amb_times.append(get_ambulation_time(len([list])))
            left_egvis.append(get_egvi_variance([list]))
            right_egvis.append(get_egvi_variance([swap_foot_indices(list)]))
        
        cv.imshow("Image", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    feature_vector = [
        np.mean(step_means),
        np.mean(velocities),
        np.mean(cadences),
        np.mean(amb_times),
        np.mean(left_egvis),
        np.mean(right_egvis),
        get_mean_egvi(np.mean(left_egvis), np.mean(right_egvis))
    ]
    
    percprediction = model.predict_proba([feature_vector]) 
    prediction2 = model.predict([feature_vector]) 
    
    cap.release()
    cv.destroyAllWindows()
    return render_template('results.html',prediction = prediction2[0],percprediction = percprediction[0][1] * 100)

