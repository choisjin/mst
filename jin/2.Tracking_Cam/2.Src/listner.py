#!/usr/bin/env python
import cv2
import rospy, time
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

rospy.init_node('ras_cam_topic_subcriber', anonymous=True)
roscam=rospy.Subscriber('/usb_cam/image_raw', Image, queue_size=1)
bridge = CvBridge()
cv_image = bridge.imgmsg_to_cv2(roscam, "bgr8")
cap = cv2.VideoCapture(cv_image)

while True:
    ret, img = cap.read()

    cv2.imshow('video', img) 
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()




