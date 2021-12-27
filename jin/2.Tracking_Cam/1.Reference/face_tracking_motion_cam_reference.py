
from __future__ import division
import time
import numpy as np
import cv2 # opencv 설치는 https://blog.naver.com/aul-_-/221449333926 참고.
import Adafruit_PCA9685 # adafruit pca9685모듈 라이브러리 설치는 https://blog.naver.com/aul-_-/221455708219 참고.
import picamera
pwm = Adafruit_PCA9685.PCA9685() 

servo_x = 90
servo_y = 90

pwm.set_pwm(1, 0, servo_x) #servo_x를 오른쪽에 위치.
pwm.set_pwm(0, 0, servo_y) #servo_y를 위쪽을 향하게 위치.
            
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

# Cascades 디렉토리의 haarcascade_frontalface_default.xml 파일을 Classifier로 사용
faceCascade = cv2.CascadeClassifier('/home/pi/ct/haarcascades/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
while True:
    ret, img = cap.read()
    img = cv2.flip(img, 0) # 좌우반전
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
        print('(',x,',',y,')') # '( x , y )'형태로 x와 y의 위치를 터미널 혹은 프롬프트에 출력.
        
        servo_x = int(x+w/2) # servo_x의 값을 얼굴을 캡처하는 사각형의 x좌표에 얼굴을 캡처하는 사각형의 밑변의 길이 나누기2 만큼 더한 값 으로  설정.
        servo_y = int(y+h/2) # servo_y의 값을 얼굴을 캡처하는 사각형의 y좌표에 얼굴을 캡처하는 사각형의 높이의 나누기2 만큼  더한 값 으로 설정.
        pwm.set_pwm(1, 0, servo_x) # servo_x의 값에 따라 1번모터를 움직임.
        pwm.set_pwm(0, 0, servo_y) # servo_y의 값에 따라 0번모터를 움직임.
        
    cv2.imshow('video', img) # video라는 이름으로 출력
    k = cv2.waitKey(1) & 0xff
    if k == 27: # press 'ESC' to quit # ESC를 누르면 종료
        pwm.set_pwm(1, 0, 130) # 모터의 안전을 위해 서보를 다시 처음 자리로 위치.
        pwm.set_pwm(0, 0, 130) # 모터의 안전을 위해 서보를 다시 처음 자리로 위치.
        break
cap.release()
cv2.destroyAllWindows()

# 이 코드는 여러 오픈소스 코드를 섞고, 내가 추가하고 수정하고, 수정함.
# 촤종 작성자 by 나  https://blog.naver.com/aul-_-/
