
import cv2 
import Adafruit_PCA9685 

servo_x = 320   # servo_x defalt position
servo_y = 390   # servo_y defalt position

pwm = Adafruit_PCA9685.PCA9685() 
pwm.set_pwm(1, 0, servo_x)  # servo_x positionin itialize
pwm.set_pwm(0, 0, servo_y)  # servo_y positionin itialize

pwm.set_pwm_freq(60)            

faceCascade = cv2.CascadeClassifier('/home/pi/mst/jin/2.Tracking_Cam/1.Reference/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

midScreenX = (640/2)    # screen x mid
midScreenY = (480/2)    # screen y mid
midScreenWindow = 25    # correction

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

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

        if servo_x1 < midScreenX-midScreenWindow:
            servo_x += 1
            pwm.set_pwm(1, 0, servo_x)

        elif servo_x1 > midScreenX+midScreenWindow:
            servo_x -= 1
            pwm.set_pwm(1, 0, servo_x)

        if servo_y1 > midScreenY+midScreenWindow:
            servo_y += 1
            pwm.set_pwm(0, 0, servo_y)

        elif servo_y1 < midScreenY-midScreenWindow:
            servo_y -= 1
            pwm.set_pwm(0, 0, servo_y)
        
    cv2.imshow('video', img) 
    k = cv2.waitKey(1) & 0xff
    if k == 27: 
        pwm.set_pwm(1, 0, 320) 
        pwm.set_pwm(0, 0, 390) 
        break
cap.release()
cv2.destroyAllWindows()


