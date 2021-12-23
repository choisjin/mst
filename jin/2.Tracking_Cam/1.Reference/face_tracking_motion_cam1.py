
from __future__ import division
import time
import numpy as np
import cv2 
import Adafruit_PCA9685 
import picamera


pwm = Adafruit_PCA9685.PCA9685() 

servo_x = 320
servo_y = 390

pwm.set_pwm(1, 0, servo_x)
pwm.set_pwm(0, 0, servo_y)
            
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)


faceCascade = cv2.CascadeClassifier('/home/pi/mst/jin/2.Tracking_Cam/1.Reference/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(60, 60)
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        
        servo_x1 = int(x+w/2)
        servo_y1 = int(y+h/2)
        
        # print('("Box :",',x,',',y,')')
        # print('("Box :",',w,',',h,')')
        print('("Mot :",',servo_x1,',',servo_y1,')')

        #pwm.set_pwm(1, 0, servo_x1) 
        #pwm.set_pwm(0, 0, servo_y1) 
        
    cv2.imshow('video', img) 
    k = cv2.waitKey(1) & 0xff
    if k == 27: 
        pwm.set_pwm(1, 0, servo_x) 
        pwm.set_pwm(0, 0, servo_y) 
        break
cap.release()
cv2.destroyAllWindows()


