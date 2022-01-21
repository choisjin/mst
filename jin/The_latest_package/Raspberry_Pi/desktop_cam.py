#-*- coding:utf-8 -*-
import rospy, cv2
from std_msgs.msg import UInt16MultiArray
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from multiprocessing import Process


global Camera_number
Camera_number = '1'

class Cam_Publisher():
    def __call__(self):
        cap = cv2.VideoCapture(1)               
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        cap.set(cv2.CAP_PROP_FPS, 20)    
        
        rospy.init_node("cam_pub", anonymous=True)
        image_pub = rospy.Publisher("cam_num%s" % Camera_number, Image, queue_size=1)
        bridge = CvBridge()

        while not rospy.is_shutdown():
            ret, cv_image = cap.read()
            image_pub.publish(bridge.cv2_to_imgmsg(cv_image, "bgr8"))

        cap.release()
        cv2.destroyAllWindows()

    # def __def__(self):
    #     print("p1_exit")
        
if __name__ == '__main__':
    init = Cam_Publisher()
