# Gesticulation (remote mouse)
The Gesticulation project uses the versatility of computer vision, machine learning and image processing to improve quality of life.
It allows for non-contact manipulation of the mouse cursor and recreating its work using pre-programmed hand gestures thanks to *MediaPipe* library.
It serves not only as a wireless computer mouse but also has some minor advantages, such as: changing the general volume of the device and the ability to run the built-in on-screen keyboard.
Everything has been implemented in the *Python* environment and converted to the runtime application (.exe file).

# Libraries:
- *PyAutoGUI* - screen keyboard minimization (0.9.53),
- *Tkinter* - window application (GUI) (8.6),
- *OpenCV* - image reading and modification (4.5.3.56),
- *time* - reading the operation execution time,
- *mouse* - restore the functionality of the mouse (0.7.1),
- *subprocess* - launching the screen keyboard,
- *Pynput* - manipulation of sound (1.7.3),
- *NumPy* - mathematical operations (1.21.2),
- *MediaPipe* - hand detection and reading (0.8.7.3),
- *PyInstaller* - convert program to executable file (4.5.1).

# Requirements:
- webcam,
- introduction of the executable application (.exe) to the anti-virus exceptions,
- change the on-screen keyboard settings to "activate keys with pointer",
- Windows operating system.

# Four built-in modes:
## Calibration mode
Program starts with displaying the camera view including the calibration window (red rectangle).
In order to start the mouse mode with the use of gestures, it is necessary to capture in the calibration window all 21 read points of the hand, visualized on the screen.
Then, mouse cursor is moved to the center of the monitor and next mode is activated.

<p align="center">
  <img src="https://user-images.githubusercontent.com/91888660/136264160-da4d97e8-2412-4c43-80fe-77d2c38fba06.png">
</p>

## Mouse mode
The mouse mode allows you to freely manipulate cursor within the visibility of the camera. Due to the limited angle of view of the camera,
the following were defined: small, medium and large error trials that deﬁnes the speed of cursor movement, i.e. the faster user moves his hand,
the greater distance cursor will travel, allowing the screen edge to be grasped. User has the following actions at his disposal: left mouse button (LMB),
right mouse button (RMB), moving the mouse wheel up, moving the mouse wheel down, double pressing the mouse button and the ability to launch the menu.
Mouse actions were defined as the approach of two specific points of the hand to each other (the moment of touching the fingers or a gesture).

<p align="center">
  <img src="https://user-images.githubusercontent.com/91888660/136264165-6e503d06-9c8f-48d8-935c-87f166cb3007.png">
</p>

## Sound mode
The sound mode allows you to adjust the volume of the entire device. User has 3 actions at his disposal: the left mouse button,
which allows you to interact with the menu, mute the device and volume up the device.

## Menu mode
In the menu mode, there are 2 actions available to the user: left mouse button and holding the left button. The menu allows you to perform the following actions:
- switching between mouse mode and volume mode,
- stop reading gestures,
- launching the built-in on-screen keyboard of Windows (**function testing stage**),
- interventions and changes to selected program parameters and mouse actions
- exiting the program.

<p align="center">
  <img src="https://user-images.githubusercontent.com/91888660/136264167-b832d504-bbf7-4dd5-b498-0f74d5e01d22.png">
</p>

# Control:
Controls are included in the additional file: "Gesticulation - control.pdf"

# Do you want to check how the current state of the application works?
- Download the zipped folder from the link: https://drive.google.com/drive/folders/1cF2S-Olz00viQD7ILmyrrXNojEKPrhjK?usp=sharing,
- Run the file: `Gesticulation\dist\main.exe`,
- Submit feedback.
