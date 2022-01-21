import rospy
import cv2

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 20)

rospy.init_node("cam_pub", anonymous=True)
image_pub = rospy.Publisher("cam_num1", Image, queue_size=1)

bridge = CvBridge()

while not rospy.is_shutdown():
    ret, cv_image = cap.read()
    image_pub.publish(bridge.cv2_to_imgmsg(cv_image, "bgr8"))

cap.release()
cv2.destroyAllWindows()