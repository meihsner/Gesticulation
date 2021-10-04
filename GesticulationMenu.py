# Author: mgr inż. Adam Meihsner
import pyautogui
from tkinter import *
import subprocess
import cv2


class Menu:
    def __init__(self, mouse_object, volume_object, cap, cal_window):
        self.root = Tk()
        self.root.title('Gesticulation Menu')
        self.root.geometry("260x590")
        self.root.configure(bg='LightSteelBlue4')
        self.root.attributes("-topmost", True)
        self.state = 'Preparing'
        self.buttons = []
        self.scales = []
        self.check_buttons = []
        self.loop = False
        self.main_menu(mouse_object, volume_object, cap, cal_window)

    def main_menu(self, mouse_object, volume_object, cap, cal_window):
        volume_button = self.add_button("Change volume via gesticulation",
                                        lambda: self.move_to_volume(mouse_object, volume_object, cap, cal_window))
        pause_button = self.add_button("Pause / Run gesticulation program",
                                       lambda: self.pause_program(mouse_object))
        virtual_keyboard_button = self.add_button("Run virtual keyboard",
                                                  lambda: self.virtual_keyboard(mouse_object,
                                                                                volume_object, cap, cal_window))
        options_button = self.add_button("Options", lambda: self.options(mouse_object, volume_object, cap, cal_window))
        exit_button = self.add_button("Exit program", lambda: self.exit_program(cap))
        if cal_window.state != "calibration":
            cal_window.state = "menu_mode"

    def options(self, mouse_object, volume_object, cap, cal_window):
        if len(self.check_buttons) > 0:
            for ele in self.check_buttons:
                ele.destroy()
        for ele in self.buttons:
            ele.destroy()

        mouse_speed = IntVar()
        mouse_click_thresh = IntVar()
        menu_pop_thresh = IntVar()
        volume_click_thresh = IntVar()
        pause_time = IntVar()

        scale_mouse_speed = self.add_scale(mouse_speed, 0, 100, HORIZONTAL, "Mouse sensitivity")
        scale_mouse_speed.set(mouse_object.mouse_speed_modifier)
        scale_mouse_click_thresh = self.add_scale(mouse_click_thresh, 0, 100, HORIZONTAL, "Mouse click threshold")
        scale_mouse_click_thresh.set(mouse_object.distance_thresh)
        scale_menu_pop_thresh = self.add_scale(menu_pop_thresh, 0, 100, HORIZONTAL, "Pop menu threshold")
        scale_menu_pop_thresh.set(mouse_object.menu_thresh)
        scale_volume_click_thresh = self.add_scale(volume_click_thresh, 0, 100, HORIZONTAL, "Volume click threshold")
        scale_volume_click_thresh.set(volume_object.distance_thresh)
        scale_pause_time = self.add_scale(pause_time, 0, 100, HORIZONTAL, "Interval between clicks")
        scale_pause_time.set(mouse_object.click_pause_time)
        button_accept_changes = self.add_button("Accept",
                                                lambda: self.accept_option_changes(mouse_object, volume_object,
                                                                                   mouse_speed, mouse_click_thresh,
                                                                                   menu_pop_thresh,
                                                                                   volume_click_thresh,
                                                                                   pause_time))
        reset_options_button = self.add_button("Reset options",
                                               lambda: self.reset_to_default_options(mouse_object, volume_object, 1))
        options_next_page_button = self.add_button("Next page",
                                                   lambda: self.options_next_page(mouse_object, volume_object,
                                                                                  cap, cal_window))
        back_to_menu_button = self.add_button("Back to menu",
                                              lambda: self.back_to_menu_from_options(mouse_object, volume_object,
                                                                                     cap, cal_window, 1))

    def options_next_page(self, mouse_object, volume_object, cap, cal_window):
        for ele in self.buttons:
            ele.destroy()
        for ele in self.scales:
            ele.destroy()

        left_click = IntVar()
        right_click = IntVar()
        wheel_up = IntVar()
        wheel_down = IntVar()
        double_click = IntVar()

        left_click_cb = self.add_checkbutton(text="Left click", variable=left_click)
        self.check_current_mouse_key_state(left_click_cb, mouse_object.left_click_state)
        right_click_cb = self.add_checkbutton(text="Right click", variable=right_click)
        self.check_current_mouse_key_state(right_click_cb, mouse_object.right_click_state)
        wheel_up_cb = self.add_checkbutton(text="Wheel up", variable=wheel_up)
        self.check_current_mouse_key_state(wheel_up_cb, mouse_object.wheel_up_state)
        wheel_down_cb = self.add_checkbutton(text="Wheel down", variable=wheel_down)
        self.check_current_mouse_key_state(wheel_down_cb, mouse_object.wheel_down_state)
        double_click_cb = self.add_checkbutton(text="Double click", variable=double_click)
        self.check_current_mouse_key_state(double_click_cb, mouse_object.double_click_state)

        button_accept_changes = self.add_button("Accept",
                                                lambda: self.accept_option_changes_second_page(mouse_object, left_click,
                                                                                               right_click, wheel_up,
                                                                                               wheel_down,
                                                                                               double_click))
        reset_options_button = self.add_button("Reset options",
                                               lambda: self.reset_to_default_options(mouse_object, volume_object, 2))
        options_previous_page_button = self.add_button("Previous page",
                                                       lambda: self.options(mouse_object, volume_object,
                                                                            cap, cal_window))
        back_to_menu_button = self.add_button("Back to menu",
                                              lambda: self.back_to_menu_from_options(mouse_object, volume_object,
                                                                                     cap, cal_window, 2))

    def check_current_mouse_key_state(self, checkbutton, variable):
        if variable == 1:
            checkbutton.select()
        else:
            checkbutton.deselect()

    def add_checkbutton(self, text, variable):
        check_button = Checkbutton(self.root, text=text, variable=variable, height=0, width=0)
        check_button.pack(fill='both', expand=True)
        self.check_buttons.append(check_button)
        return check_button

    def add_scale(self, variable, from_val, to_val, orientation, label):
        scale = Scale(self.root, variable=variable, from_=from_val, to=to_val, orient=orientation, label=label)
        scale.pack(fill='both', expand=True)
        self.scales.append(scale)
        return scale

    def add_button(self, button_text, button_command):
        button = Button(self.root, text=button_text, command=button_command, bg='LightSteelBlue2', fg='black')
        button.pack(fill='both', expand=True)
        self.buttons.append(button)
        return button

    def reset_to_default_options(self, mouse_object, volume_object, page):
        if page == 1:
            mouse_object.mouse_speed_modifier = mouse_object.default_mouse_speed_modifier
            mouse_object.distance_thresh = mouse_object.default_distance_thresh
            mouse_object.menu_thresh = mouse_object.default_menu_thresh
            volume_object.distance_thresh = volume_object.default_distance_thresh
            mouse_object.click_pause_time = mouse_object.default_click_pause_time
            self.scales[0].set(mouse_object.default_mouse_speed_modifier)
            self.scales[1].set(mouse_object.default_distance_thresh)
            self.scales[2].set(mouse_object.default_menu_thresh)
            self.scales[3].set(volume_object.default_distance_thresh)
            self.scales[4].set(mouse_object.default_click_pause_time)

        if page == 2:
            mouse_object.left_click_state = mouse_object.default_left_click_state
            mouse_object.right_click_state = mouse_object.default_right_click_state
            mouse_object.wheel_up_state = mouse_object.default_wheel_up_state
            mouse_object.wheel_down_state = mouse_object.default_wheel_down_state
            mouse_object.double_click_state = mouse_object.default_double_click_state

    def accept_option_changes(self, mouse_object, volume_object, mouse_speed, mouse_click_thresh,
                              menu_pop_thresh, volume_click_thresh, pause_time):
        mouse_object.mouse_speed_modifier = mouse_speed.get()
        mouse_object.distance_thresh = mouse_click_thresh.get()
        mouse_object.menu_thresh = menu_pop_thresh.get()
        volume_object.distance_thresh = volume_click_thresh.get()
        mouse_object.click_pause_time = pause_time.get()

    def accept_option_changes_second_page(self, mouse_object, left_click, right_click,
                                          wheel_up, wheel_down, double_click):
        mouse_object.left_click_state = left_click.get()
        mouse_object.right_click_state = right_click.get()
        mouse_object.wheel_up_state = wheel_up.get()
        mouse_object.wheel_down_state = wheel_down.get()
        mouse_object.double_click_state = double_click.get()

    def virtual_keyboard(self, mouse_object, volume_object, cap, cal_window):
        subprocess.Popen("osk", shell=True)
        for ele in self.buttons:
            ele.destroy()
        volume_button = self.add_button("Change volume via gesticulation",
                                        lambda: self.move_to_volume(mouse_object, volume_object, cap, cal_window))
        pause_button = self.add_button("Pause / Run gesticulation program", lambda: self.pause_program(mouse_object))
        virtual_keyboard_button = self.add_button("Minimize virtual keyboard",
                                                  lambda: self.back_to_menu_from_keyboard(mouse_object, volume_object,
                                                                                          cap, cal_window))
        options_button = self.add_button("Options", lambda: self.options(mouse_object, volume_object, cap, cal_window))
        exit_button = self.add_button("Exit program", lambda: self.exit_program(cap))

    def hide_window(self):
        self.state = 'Hidden'
        self.root.withdraw()

    def show_window(self):
        self.state = 'Showed'
        self.root.deiconify()

    def pause_program(self, mouse_object):
        if mouse_object.paused == "no":
            mouse_object.paused = "yes"
        else:
            mouse_object.paused = "no"

    def move_to_volume(self, mouse_object, volume_object, cap, cal_window):
        for ele in self.buttons:
            ele.destroy()
        gesticulation_button = self.add_button("Back to gesticulation",
                                               lambda: self.back_to_menu(mouse_object, volume_object,
                                                                         cap, cal_window))
        pause_button = self.add_button("Pause / Run gesticulation program", lambda: self.pause_program(mouse_object))
        virtual_keyboard_button = self.add_button("Run virtual keyboard",
                                                  lambda: self.virtual_keyboard(mouse_object, volume_object,
                                                                                cap, cal_window))
        options_button = self.add_button("Options", lambda: self.options(mouse_object, volume_object, cap, cal_window))
        exit_button = self.add_button("Exit program", lambda: self.exit_program(cap))

        cal_window.state = "volume_mode"
        self.state = "volume"

    def back_to_menu(self, mouse_object, volume_object, cap, cal_window):
        for ele in self.buttons:
            ele.destroy()
        self.main_menu(mouse_object, volume_object, cap, cal_window)

    def back_to_menu_from_options(self, mouse_object, volume_object, cap, cal_window, page):
        for ele in self.buttons:
            ele.destroy()
        for ele in self.scales:
            ele.destroy()
        if page == 2:
            for ele in self.check_buttons:
                ele.destroy()
        self.main_menu(mouse_object, volume_object, cap, cal_window)

    def back_to_menu_from_keyboard(self, mouse_object, volume_object, cap, cal_window):
        for ele in self.buttons:
            ele.destroy()
        pyautogui.keyDown('win')
        pyautogui.press('d')
        self.main_menu(mouse_object, volume_object, cap, cal_window)

    def exit_program(self, cap):
        for ele in self.buttons:
            ele.destroy()
        self.root.destroy()
        cap.release()
        cv2.destroyAllWindows()
        exit()
