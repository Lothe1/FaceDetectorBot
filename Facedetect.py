#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2

import numpy as np

from picamera.array import PiRGBArray

from picamera import PiCamera

from time import sleep

import RPi.GPIO as GPIO

import time

GPIO.setmode(GPIO.BOARD)

control_pins2 = [13, 11, 15, 12]

control_pins = [33, 31, 35, 32]

for pin in control_pins:

    GPIO.setup(pin, GPIO.OUT)

    GPIO.output(pin, 0)

for pin2 in control_pins2:

    GPIO.setup(pin2, GPIO.OUT)

    GPIO.output(pin2, 0)

xAngle = 0

yAngle = 0

halfstep_seq_right = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1],
    ]

halfstep_seq_left = [
    [1, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 1, 1],
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 0],
    [1, 1, 0, 0],
    [1, 0, 0, 0],
    ]


def turnLeft():

    for halfstep in range(8):

        for pin in range(4):

            GPIO.output(control_pins[pin],
                        halfstep_seq_right[halfstep][pin])

        time.sleep(0.01)


def turnRight():

    for halfstep in range(8):

        for pin in range(4):

            GPIO.output(control_pins[pin],
                        halfstep_seq_left[halfstep][pin])

        time.sleep(0.01)


def turnUp():

    for halfstep in range(8):

        for pin2 in range(4):

            GPIO.output(control_pins2[pin2],
                        halfstep_seq_right[halfstep][pin2])

        time.sleep(0.01)


def turnDown():

    for halfstep in range(8):

        for pin2 in range(4):

            GPIO.output(control_pins2[pin2],
                        halfstep_seq_left[halfstep][pin2])

        time.sleep(0.01)


path = '/home/pi/test/static/myimage.jpg'

face_cascade = \
    cv2.CascadeClassifier('/home/pi/test/data/haarcascade_frontalface_default.xml'
                          )

if face_cascade.empty():

    print 'invalid'

try:

    camera = PiCamera()

    screenWidth = 320

    screenHeight = 240

    camera.resolution = (screenWidth, screenHeight)

    camera.framerate = 24

    camera.rotation = 180

    rawCapture = PiRGBArray(camera, size=(320, 240))

    time.sleep(0.1)

    for frame in camera.capture_continuous(rawCapture, format='bgr',
            use_video_port=True):

        faceTake = frame.array

        faceGray = cv2.cvtColor(faceTake, cv2.COLOR_BGR2GRAY)

        faceDetect = face_cascade.detectMultiScale(faceGray, 1.3, 5)

        cv2.imshow('frame', faceTake)

        for (x, y, w, h) in faceDetect:

            midFace = x + w / 2

            if midFace < screenWidth / 2 - 15 and xAngle < 20:

                turnRight()

                xAngle = xAngle + 1

                print 'TURNING LEFT'
            elif midFace > screenWidth / 2 + 15 and xAngle > -20:

                turnLeft()

                xAngle = xAngle - 1

                print 'TURNING RIGHT'

            midFace = y + h / 2

            if midFace < screenHeight / 2 - 15 and yAngle < 15:

                turnDown()

                yAngle = yAngle + 1

                print 'TURNING UP'
            elif midFace > screenHeight / 2 + 15 and yAngle > -15:

                turnUp()

                yAngle = yAngle - 1

                print 'TURNING DOWN'

            break

        sleep(0.01)

        key = cv2.waitKey(1) & 0xFF

        rawCapture.truncate(0)

        if key == ord('q'):

            break
finally:

    cv2.destroyAllWindows()

    if xAngle > 0:

        while xAngle > 0:

            turnLeft()

            xAngle = xAngle - 1
    elif xAngle < 0:

        while xAngle < 0:

            turnRight()

            xAngle = xAngle + 1

    if yAngle > 0:

        while yAngle > 0:

            turnUp()

            yAngle = yAngle - 1
    elif yAngle < 0:

        while yAngle < 0:

            turnDown()

            yAngle = yAngle + 1

    GPIO.cleanup()
