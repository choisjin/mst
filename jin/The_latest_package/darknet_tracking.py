from ctypes import *
import random
import os
import cv2, rospy
import time
import darknet
import argparse
from threading import Thread, enumerate
from queue import Queue
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import UInt16MultiArray

class Darknet_Start():
    def __init__(self, camera, train_path):
        print('start')
        self.train_path = train_path
        
        self.frame_queue = Queue()
        self.darknet_image_queue = Queue(maxsize=1)
        self.detections_queue = Queue(maxsize=1)
        self.fps_queue = Queue(maxsize=1 )
    
        self.args = self.parser() 
        self.check_arguments_errors(self.args)
        self.network, self.class_names, self.class_colors = darknet.load_network(
                self.args.config_file,
                self.args.data_file,
                self.args.weights,
                batch_size=1
            )
        self.darknet_width = darknet.network_width(self.network)
        self.darknet_height = darknet.network_height(self.network)

        #rospy.init_node('cam_sub_%s' % camera, anonymous = False)
        self._sub = rospy.Subscriber('/cam_num_%s' % camera, Image, self.callback, queue_size=1)
        print('topic')
        self.bridge = CvBridge()
        #rospy.spin()
    def parser(self):
        parser = argparse.ArgumentParser(description="YOLO Object Detection")
        parser.add_argument("--weights", default=self.train_path,
                            help="yolo weights path")
        parser.add_argument("--dont_show", action='store_true',
                            help="windown inference display. For headless systems")
        parser.add_argument("--ext_output", action='store_true',
                            help="display bbox coordinates of detected objects")
        parser.add_argument("--config_file", default="/home/jin/darknet/cfg/yolov4-obj.cfg",
                            help="path to config file")
        parser.add_argument("--data_file", default="/home/jin/darknet/data/obj.data",
                            help="path to data file")
        parser.add_argument("--thresh", type=float, default=.25,
                            help="remove detections with confidence below this value")
        return parser.parse_args()

    def str2int(video_path):
        """
        argparse returns and string althout webcam uses int (0, 1 ...)
        Cast to int if needed
        """
        try:
            return int(video_path)
        except ValueError:
            return video_path

    def check_arguments_errors(self, args):
        assert 0 < args.thresh < 1, "Threshold should be a float between zero and one (non-inclusive)"
        if not os.path.exists(args.config_file):
            raise(ValueError("Invalid config path {}".format(os.path.abspath(args.config_file))))
        if not os.path.exists(args.weights):
            raise(ValueError("Invalid weight path {}".format(os.path.abspath(args.weights))))
        if not os.path.exists(args.data_file):
            raise(ValueError("Invalid data file path {}".format(os.path.abspath(args.data_file))))

    def convert2relative(self, bbox):
        """
        YOLO format use relative coordinates for annotation
        """
        x, y, w, h  = bbox
        _height     = self.darknet_height
        _width      = self.darknet_width
        return x/_width, y/_height, w/_width, h/_height

    def convert2original(self, image, bbox):
        x, y, w, h = self.convert2relative(bbox)

        image_h, image_w, __ = image.shape

        orig_x       = int(x * image_w)
        orig_y       = int(y * image_h)
        orig_width   = int(w * image_w)
        orig_height  = int(h * image_h)

        bbox_converted = (orig_x, orig_y, orig_width, orig_height)

        return bbox_converted

    def convert4cropping(self, image, bbox):
        x, y, w, h = self.convert2relative(bbox)

        image_h, image_w, __ = image.shape

        orig_left    = int((x - w / 2.) * image_w)
        orig_right   = int((x + w / 2.) * image_w)
        orig_top     = int((y - h / 2.) * image_h)
        orig_bottom  = int((y + h / 2.) * image_h)

        if (orig_left < 0): orig_left = 0
        if (orig_right > image_w - 1): orig_right = image_w - 1
        if (orig_top < 0): orig_top = 0
        if (orig_bottom > image_h - 1): orig_bottom = image_h - 1

        bbox_cropping = (orig_left, orig_top, orig_right, orig_bottom)

        return bbox_cropping

    def callback(self, data):
        print('callback')
        self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")

        
        frame_rgb = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (self.darknet_width, self.darknet_height),
                                   interpolation=cv2.INTER_LINEAR)
        self.frame_queue.put(self.cv_image)
        img_for_detect = darknet.make_image(self.darknet_width, self.darknet_height, 3)
        darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())
        self.darknet_image_queue.put(img_for_detect)

        
        darknet_image = self.darknet_image_queue.get()
        prev_time = time.time()
        detections = darknet.detect_image(self.network, self.class_names, darknet_image, thresh=self.args.thresh)
        self.detections_queue.put(detections)
        self.fps = int(1/(time.time() - prev_time))
        self.fps_queue.put(self.fps)
        print("FPS: {}".format(self.fps))
        darknet.print_detections(detections, self.args.ext_output)
        darknet.free_image(darknet_image)


        random.seed(3)  # deterministic bbox colors

        frame = self.frame_queue.get()
        detections = self.detections_queue.get()
        self.fps = self.fps_queue.get()
        detections_adjusted = []
        if frame is not None:
            for label, confidence, bbox in detections:
                bbox_adjusted = self.convert2original(frame, bbox)
                detections_adjusted.append((str(label), confidence, bbox_adjusted))
            image = darknet.draw_boxes(detections_adjusted, frame, self.class_colors)
            print('image')
            return image
    
    # def image_return(self):        
        # self.image