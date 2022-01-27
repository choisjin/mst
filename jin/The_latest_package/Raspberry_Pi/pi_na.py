#-*- coding:utf-8 -*-
import rospy, cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from multiprocessing import Process

global Camera_number
Camera_number = '3'

class Cam_Publisher():
    def __call__(self):
        cap = cv2.VideoCapture(1)               
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        cap.set(cv2.CAP_PROP_FPS, 30)    
        
        rospy.init_node("cam_pub_%s" % Camera_number, anonymous = False)
        image_pub = rospy.Publisher("cam_num_%s" % Camera_number, Image, queue_size=1)

        bridge = CvBridge()

        while not rospy.is_shutdown():
            ret, cv_image = cap.read()
            image_pub.publish(bridge.cv2_to_imgmsg(cv_image, "bgr8"))

        cap.release()
        cv2.destroyAllWindows()

    def __del__(self):
        print("p1_exit")
        
try:    
    p1 = Process(target = Cam_Publisher())          # Cam_data Publisher


    p1.start()


except KeyboardInterrupt:
    print("Ctrl + C")

finally:
    print("exit program")
