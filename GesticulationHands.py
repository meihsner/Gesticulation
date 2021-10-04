# Source: https://www.analyticsvidhya.com/blog/2021/07/building-a-hand-tracking-system-using-opencv/
import mediapipe as mp


class Hands:
    def __init__(self, mode, hands_number, detection_conf, tracking_conf):
        self.mode = mode
        self.hands_number = hands_number
        self.detection_conf = detection_conf
        self.tracking_conf = tracking_conf

        self.declare_hands_object = mp.solutions.hands
        self.hands = self.declare_hands_object.Hands(static_image_mode=self.mode,
                                                     max_num_hands=self.hands_number,
                                                     min_detection_confidence=self.detection_conf,
                                                     min_tracking_confidence=self.tracking_conf)
        self.draw_hands = mp.solutions.drawing_utils
        self.results = []

    def find_hands(self, image, draw):
        self.results = self.hands.process(image)
        if draw:
            if self.results.multi_hand_landmarks:
                for handLms in self.results.multi_hand_landmarks:
                    self.draw_hands.draw_landmarks(image, handLms, self.declare_hands_object.HAND_CONNECTIONS)
        return image

    def find_position(self, image, hand_number):
        landmarks = []
        if self.results.multi_hand_landmarks:
            hand_landmarks = self.results.multi_hand_landmarks[hand_number]
            for id_of_landmarks, lm in enumerate(hand_landmarks.landmark):
                N, M, c = image.shape
                cx, cy = int(lm.x * M), int(lm.y * N)
                landmarks.append([id_of_landmarks, cx, cy])
        return landmarks
