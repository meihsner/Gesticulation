# Author: mgr inż. Adam Meihsner
import time
import mouse
import cv2
import numpy as np


class Mouse:
    def __init__(self, resolution_width, resolution_height):
        self.mouse_speed_modifier = 0
        self.default_mouse_speed_modifier = 0
        self.coordinate_x_correction = 5
        self.coordinate_y_correction = 5
        self.distance_thresh = 40
        self.default_distance_thresh = 40
        self.menu_thresh = 25
        self.default_menu_thresh = 25
        self.start_hand_position = (resolution_width / 2), (resolution_height / 2)
        self.start_mouse_position = (resolution_width / 2), (resolution_height / 2)
        self.current_hand_position = [0, 0]
        self.current_mouse_position = [0, 0]
        self.previous_hand_position = self.start_hand_position
        self.previous_mouse_position = self.start_mouse_position
        #  self.state = "Released"
        self.paused = "no"
        self.double_click = "no"
        self.timer = time.time()
        self.click_pause_time = 1
        self.default_click_pause_time = 1
        self.keep = "no"
        self.left_click_state = 1
        self.right_click_state = 1
        self.wheel_up_state = 1
        self.wheel_down_state = 1
        self.double_click_state = 1
        self.default_left_click_state = 1
        self.default_right_click_state = 1
        self.default_wheel_up_state = 1
        self.default_wheel_down_state = 1
        self.default_double_click_state = 1

        self.palms_coordinates = []
        for i in range(0, 21):
            self.palms_coordinates.append([0, 0])

    def update_current_position(self, landmarks):
        if len(landmarks) > 0:
            x_hand = landmarks[9][1]
            y_hand = landmarks[9][2]
            self.current_hand_position = (x_hand, y_hand)
            self.current_mouse_position = mouse.get_position()

    def update_previous_position(self, landmarks):
        if len(landmarks) > 0:
            self.previous_hand_position = self.current_hand_position
            self.previous_mouse_position = self.current_mouse_position

    def move(self, landmarks):
        if len(landmarks) > 0:
            if self.paused == "no":
                small_move_errors = [2, 1, 0, -1, -2]
                medium_move_errors = [5, 4, 3, -3, -4, -5]
                move_x = self.current_hand_position[0] - self.previous_hand_position[0]
                move_y = self.current_hand_position[1] - self.previous_hand_position[1]

                if move_x in small_move_errors:
                    self.coordinate_x_correction = 2 + self.mouse_speed_modifier
                elif move_x in medium_move_errors:
                    self.coordinate_x_correction = 3 + self.mouse_speed_modifier
                else:
                    self.coordinate_x_correction = 5 + self.mouse_speed_modifier

                if move_y in small_move_errors:
                    self.coordinate_y_correction = 2 + self.mouse_speed_modifier
                elif move_y in medium_move_errors:
                    self.coordinate_y_correction = 3 + self.mouse_speed_modifier
                else:
                    self.coordinate_y_correction = 5 + self.mouse_speed_modifier

                mouse.move(self.current_mouse_position[0] + self.coordinate_x_correction * move_x,
                           self.current_mouse_position[1] + self.coordinate_y_correction * move_y,
                           absolute=True, duration=0)

    def left_click(self, image, landmarks, finger_id1, finger_id2, verify):
        if self.left_click_state == 1:
            mouse_click(self, image, landmarks, finger_id1, finger_id2, verify,
                        (0, 255, 0), (0, 0, 255), (20, 120), 'Left click dist: ', 'click', 'left')

    def right_click(self, image, landmarks, finger_id1, finger_id2, verify):
        if self.right_click_state == 1:
            mouse_click(self, image, landmarks, finger_id1, finger_id2, verify,
                        (0, 255, 0), (0, 0, 255), (20, 170), 'Right click dist: ', 'click', 'right')

    def scroll_up(self, image, landmarks, finger_id1, finger_id2, verify):
        if self.wheel_up_state == 1:
            mouse_click(self, image, landmarks, finger_id1, finger_id2, verify,
                        (0, 255, 0), (0, 0, 255), (20, 230), 'Scroll up dist: ', 'scroll', 'up')

    def scroll_down(self, image, landmarks, finger_id1, finger_id2, verify):
        if self.wheel_down_state == 1:
            mouse_click(self, image, landmarks, finger_id1, finger_id2, verify,
                        (0, 255, 0), (0, 0, 255), (20, 280), 'Scroll down dist: ', 'scroll', 'down')

    def keep_left(self, image, landmarks, finger_id1, finger_id2, verify):
        mouse_click(self, image, landmarks, finger_id1, finger_id2, verify,
                    (0, 255, 0), (0, 0, 255), (20, 170), 'Keep left dist: ', 'keep', 'left')

    def enable_double_click(self, image, landmarks, finger_id1, finger_id2, verify):
        if self.double_click_state == 1:
            distance = 100
            if len(landmarks) > 0:
                distance = calculate_distance(image, landmarks, finger_id1, finger_id2, (255, 0, 0),
                                              self.palms_coordinates)
                if verify:
                    if distance <= self.distance_thresh:
                        cv2.putText(image, "Double click: " + str(int(distance)), (20, 330), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.7, (0, 255, 0), 2)
                    else:
                        cv2.putText(image, "Double click: " + str(int(distance)), (20, 330), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.7, (0, 0, 255), 2)
            if distance <= self.distance_thresh:
                if time.time() - self.timer > self.click_pause_time:
                    if self.double_click == "no":
                        self.double_click = "yes"
                        self.timer = time.time()
                    else:
                        self.double_click = "no"
                        self.timer = time.time()

    def check_menu_window_distances(self, image, landmarks):
        palms_ids = [[5, 8], [9, 12], [13, 16], [17, 20]]
        selected_palms_dist = []
        if len(landmarks) > 0:
            for ele in palms_ids:
                distance = calculate_distance(image, landmarks, ele[0], ele[1], (0, 0, 255), self.palms_coordinates)
                selected_palms_dist.append(distance)
        return selected_palms_dist

    def menu_window(self, selected_palms_dist, landmarks, window):
        if len(landmarks) > 0:
            if check_list_less(selected_palms_dist, self.menu_thresh):
                if time.time() - self.timer > self.click_pause_time:
                    if window.state == 'Hidden':
                        window.loop = True
                        window.show_window()
                        window.state = 'Showed'
                    else:
                        window.hide_window()
                        window.state = 'Hidden'
                    self.timer = time.time()


def mouse_click(mouse_object, image, landmarks, finger_id1, finger_id2, verify, color1, color2,
                text_coordinates, text, mouse_type, which):
    distance = 100
    if len(landmarks) > 0:
        distance = calculate_distance(image, landmarks, finger_id1, finger_id2,
                                      (255, 0, 0), mouse_object.palms_coordinates)
        if verify:
            if distance <= mouse_object.distance_thresh:
                cv2.putText(image, text + str(int(distance)), text_coordinates, cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, color1, 2)
            else:
                cv2.putText(image, text + str(int(distance)), text_coordinates, cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, color2, 2)
    if mouse_type == "scroll":
        mouse_object.distance_thresh = 28
    else:
        mouse_object.distance_thresh = 40
    if distance <= mouse_object.distance_thresh:
        if mouse_type == "click":
            if time.time() - mouse_object.timer > mouse_object.click_pause_time:
                if mouse_object.double_click == "no":
                    mouse.click(which)
                    mouse_object.timer = time.time()
                elif mouse_object.double_click == "yes":
                    mouse.click(which)
                    mouse.click(which)
                    mouse_object.timer = time.time()
        elif mouse_type == "scroll":
            if which == "up":
                mouse.wheel(1)
            else:
                mouse.wheel(-1)
        elif mouse_type == "keep":
            if time.time() - mouse_object.timer > mouse_object.click_pause_time:
                if mouse_object.keep == "no":
                    mouse.press(which)
                    mouse_object.keep = "yes"
                    mouse_object.timer = time.time()
                else:
                    mouse.release(which)
                    mouse_object.keep = "no"
                    mouse_object.timer = time.time()

    return image


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


def check_list_less(list_to_check, value):
    verify_list = []
    for ele in list_to_check:
        if ele > value:
            verify_list.append(1)
        else:
            verify_list.append(0)
    if sum(verify_list) == 0:
        return True
    else:
        return False
