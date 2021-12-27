from std_msgs.msg import String
import rospy
import rasp_cam_subscriber

if rasp_cam_subscriber.__name__ == '__main__':
    rasp_cam_subscriber.Rasp_Cam_Subscriber()

def talker():
        pub = rospy.Publisher('chatter', String, queue_size=10)
        rospy.init_node('talker', anonymous=True)
        #rate = rospy.Rate(10) # 10hz
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        #rate.sleep()    
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass