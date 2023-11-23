import cv2
import time
target_url = 'udp://@0.0.0.0:12345'
stream = cv2.VideoCapture(target_url)
while True:
        r, f = stream.read()
        if r:
            cv2.imshow('IP Camera stream',f)
