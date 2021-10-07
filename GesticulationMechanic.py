import cv2
import time


def run_gesticulation(cap, resolution_width, resolution_height, calibration_iter, cal_window,
                      hands, gesture_mouse, gesture_volume, window):
    while True:
        if window.loop:
            window.root.update()

        start_time = time.time()
        cal_window.restart_hand_location()
        ret, image = cap.read()

        if ret:
            image = cv2.flip(image, 1)
            image = hands.find_hands(image, True)
            landmarks = hands.find_position(image, 0)
            cal_window.check_hand_location(landmarks, resolution_width, resolution_height)

            if window.state == "Hidden":
                cal_window.state = "mouse_mode"
            elif window.state == "Showed":
                cal_window.state = "menu_mode"

            if cal_window.state == "mouse_mode":
                if calibration_iter:
                    gesture_mouse.update_current_position(landmarks)
                    calibration_iter = False
                else:
                    gesture_mouse.update_previous_position(landmarks)
                    gesture_mouse.update_current_position(landmarks)
                    gesture_mouse.move(landmarks)
                    gesture_mouse.left_click(image, landmarks, 4, 8, True)
                    gesture_mouse.right_click(image, landmarks, 4, 12, True)
                    gesture_mouse.scroll_up(image, landmarks, 4, 16, True)
                    gesture_mouse.scroll_down(image, landmarks, 4, 20, True)
                    gesture_mouse.enable_double_click(image, landmarks, 4, 13, True)

                    selected_palms_dist = gesture_mouse.check_menu_window_distances(image, landmarks)
                    gesture_mouse.menu_window(selected_palms_dist, landmarks, window)

            elif cal_window.state == "menu_mode":
                gesture_mouse.update_previous_position(landmarks)
                gesture_mouse.update_current_position(landmarks)
                gesture_mouse.move(landmarks)
                gesture_mouse.left_click(image, landmarks, 4, 8, True)
                gesture_mouse.keep_left(image, landmarks, 4, 12, True)

                selected_palms_dist = gesture_mouse.check_menu_window_distances(image, landmarks)
                gesture_mouse.menu_window(selected_palms_dist, landmarks, window)

            elif cal_window.state == "calibration":
                cal_window.draw_window(image)

            elif cal_window.state == "volume_mode":
                gesture_volume.change_volume(image, landmarks, gesture_mouse)
                gesture_mouse.update_previous_position(landmarks)
                gesture_mouse.update_current_position(landmarks)
                gesture_mouse.move(landmarks)
                gesture_mouse.left_click(image, landmarks, 4, 8, True)

            if gesture_mouse.double_click == "yes":
                cv2.putText(image, "Double click enabled", (270, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (255, 255, 0), 2)
            elif gesture_mouse.double_click == "no":
                cv2.putText(image, "Double click disabled", (270, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (255, 255, 0), 2)

            current_time = time.time()
            fps = 1 / (current_time - start_time)
            cv2.putText(image, "FPS: " + str(int(fps)), (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.imshow('Gesticulation Window', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print('Cannot acquire image')
            break

    cap.release()
    cv2.destroyAllWindows()
