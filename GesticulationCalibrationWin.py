# Author: mgr inż. Adam Meihsner
import cv2
import mouse


class CalibrationWindow:
    def __init__(self, resolution_width, resolution_height):
        self.width = resolution_width
        self.height = resolution_height
        self.color = (0, 0, 255)
        self.resolution_percentage = 0.4
        self.corrected_width = int(self.resolution_percentage * self.width)
        self.corrected_height = int(self.resolution_percentage * self.height)

        self.center_x = round(resolution_width / 2)
        self.center_y = round(resolution_height / 2)

        self.x1 = self.center_x - round(self.corrected_width / 2)
        self.y1 = self.center_y - round(self.corrected_height / 2)
        self.x2 = self.center_x + round(self.corrected_width / 2)
        self.y2 = self.center_y + round(self.corrected_height / 2)

        self.verify_hand_location = []
        for i in range(21):
            self.verify_hand_location.append(0)

        self.state = "calibration"

    def draw_window(self, image):
        cv2.rectangle(image, (self.x1, self.y1), (self.x2, self.y2), self.color, 3)

    def restart_hand_location(self):
        self.verify_hand_location = [0 for ele in self.verify_hand_location]

    def check_hand_location(self, landmarks, true_resolution_width, true_resolution_height):
        if len(landmarks) > 0:
            for ele in landmarks:
                if self.x1 < ele[1] < self.x2 and self.y1 < ele[2] < self.y2:
                    self.verify_hand_location[ele[0]] = 1

            if sum(self.verify_hand_location) == 21:
                self.color = (0, 255, 0)
                if self.state == "calibration":
                    self.state = "mouse_mode"
                    mouse.move((true_resolution_width / 2), (true_resolution_height / 2), absolute=True, duration=0.2)
            else:
                self.color = (0, 0, 255)
