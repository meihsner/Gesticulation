# Author: mgr inż. Adam Meihsner
import time
from pynput.keyboard import Key, Controller
import cv2
import numpy as np


class Volume:
    def __init__(self):
        self.distance_thresh = 40
        self.default_distance_thresh = 40
        self.timer = time.time()
        self.control = Controller()
        self.state = "running"

    def volume_up(self, image, landmarks, mouse_object, finger_id1, finger_id2):
        distance = 100
        if len(landmarks) > 0:
            distance = calculate_distance(image, landmarks, finger_id1, finger_id2,
                                          (255, 0, 0), mouse_object.palms_coordinates)

        if distance <= self.distance_thresh:
            self.control.press(Key.media_volume_up)
            self.control.release(Key.media_volume_up)
            time.sleep(0.1)

    def volume_down(self, image, landmarks, mouse_object, finger_id1, finger_id2):
        distance = 100
        if len(landmarks) > 0:
            distance = calculate_distance(image, landmarks, finger_id1, finger_id2,
                                          (255, 0, 0), mouse_object.palms_coordinates)

        if distance <= self.distance_thresh:
            self.control.press(Key.media_volume_down)
            self.control.release(Key.media_volume_down)
            time.sleep(0.1)

    def change_volume(self, image, landmarks, mouse_object):
        if len(landmarks) > 0:
            self.volume_up(image, landmarks, mouse_object, 4, 12)
            self.volume_down(image, landmarks, mouse_object, 4, 16)
        elif len(landmarks) == 0:
            self.state = "paused"


def calculate_distance(image, landmarks, id1, id2, color, palms_coordinates):
    x_landmark1 = landmarks[id1][1]
    y_landmark1 = landmarks[id1][2]

    x_landmark2 = landmarks[id2][1]
    y_landmark2 = landmarks[id2][2]

    distance = np.sqrt((pow(x_landmark2-x_landmark1, 2))+(pow(y_landmark2-y_landmark1, 2)))
    cv2.circle(image, (x_landmark1, y_landmark1), 10, (0, 255, 0), 2)
    cv2.circle(image, (x_landmark2, y_landmark2), 10, (0, 255, 0), 2)
    cv2.line(image, (x_landmark1, y_landmark1), (x_landmark2, y_landmark2), color, 2)

    palms_coordinates[id1 - 1][0] = x_landmark1
    palms_coordinates[id1 - 1][1] = y_landmark1
    palms_coordinates[id2 - 1][0] = x_landmark2
    palms_coordinates[id2 - 1][1] = y_landmark2
    return distance
