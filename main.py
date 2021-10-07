# Author: mgr inż. Adam Meihsner
import GesticulationCalibrationWin
import GesticulationMenu
import GesticulationVolume
import GesticulationHands
import GesticulationMouse
import pyautogui
from GesticulationMechanic import *


def main():
    resolution = pyautogui.size()
    resolution_width = resolution[0]
    resolution_height = resolution[1]

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

    cal_window = GesticulationCalibrationWin.CalibrationWindow(800, 600)
    hands = GesticulationHands.Hands(False, 1, 0.5, 0.5)
    gesture_mouse = GesticulationMouse.Mouse(resolution_width, resolution_height)
    gesture_volume = GesticulationVolume.Volume()
    window = GesticulationMenu.Menu(gesture_mouse, gesture_volume, cap, cal_window)

    calibration_iter = True
    run_gesticulation(cap, resolution_width, resolution_height, calibration_iter, cal_window,
                      hands, gesture_mouse, gesture_volume, window)


if __name__ == "__main__":
    main()
