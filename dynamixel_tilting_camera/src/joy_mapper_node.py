#!/usr/bin/env python
import rospy
import math

from sensor_msgs.msg import Joy
from std_msgs.msg import Float64
class Joymapper(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        self.Joy = None
        rospy.loginfo("Initializing [%s]" %self.node_name)
        self.left_pan = self.mid_pan = self.right_pan = Float64()
        self.left_tilt = self.mid_tilt = self.right_tilt = Float64()
        self.left_pan.data = self.mid_pan.data = self.right_pan.data = 0.0
        self.left_tilt.data = self.mid_tilt.data = self.right_tilt.data = 0.0
        self.count = 0
        self.left_run = True
        self.mid_run = False
        self.right_run = False
        rospy.loginfo("left_camera")
        self.time=0.0
        self.temp=0.0
        #Subscribers
        self.sub_joy = rospy.Subscriber("joy", Joy, self.cbJoy, queue_size=1)

        #Publishers
        self.left_pan_pub = rospy.Publisher("left_pan_controller/command", Float64, queue_size=1)
        self.left_tilt_pub = rospy.Publisher("left_tilt_controller/command", Float64, queue_size=1)
        self.mid_pan_pub = rospy.Publisher("mid_pan_controller/command", Float64, queue_size=1)
        self.mid_tilt_pub = rospy.Publisher("mid_tilt_controller/command", Float64, queue_size=1)
        self.right_pan_pub = rospy.Publisher("right_pan_controller/command", Float64, queue_size=1)
        self.right_tilt_pub = rospy.Publisher("right_tilt_controller/command", Float64, queue_size=1)
    
    def cbJoy(self, msg):
        self.Joy = msg
        self.processButtons()
        self.processAxes()
    
    def processButtons(self):
    
        if self.Joy.buttons[4] == 1:
            
            
            self.temp = self.time
            self.time = rospy.get_time()
            #rospy.loginfo("time-temp=%lf", self.time-self.temp)
            if self.time-self.temp > 0.08:
                if self.count==2:
                    self.count = -1
                self.count = self.count+1
                
            if self.count==0:
                rospy.loginfo("left_camera %d", self.count)  
            elif self.count==1:
                rospy.loginfo("mid_camera %d", self.count) 
            elif self.count==2:
                rospy.loginfo("right_camera %d", self.count)

            
        if self.Joy.buttons[3] == 1 and self.count==0:
            rospy.loginfo("left_pan and left_tilt back to middle")
            self.left_pan.data = 0.0
            self.left_tilt.data = 0.0
            self.left_pan_pub.publish(self.left_pan)
            self.left_tilt_pub.publish(self.left_tilt)

        elif self.Joy.buttons[3] == 1 and self.count==1:
            rospy.loginfo("mid_pan and mid_tilt back to middle")
            self.mid_pan.data = 0.0
            self.mid_tilt.data = 0.0
            self.mid_pan_pub.publish(self.mid_pan)
            self.mid_tilt_pub.publish(self.mid_tilt)

        elif self.Joy.buttons[3] == 1 and self.count==2:
            rospy.loginfo("right_pan and right_tilt back to middle")
            self.right_pan.data = 0.0
            self.right_tilt.data = 0.0
            self.right_pan_pub.publish(self.right_pan)
            self.right_tilt_pub.publish(self.right_tilt)

    def processAxes(self):
        ### left camera
        if self.Joy.axes[7]>0 and self.count==0:
            self.left_tilt.data -=0.02
            self.left_tilt.data = -0.7 if self.left_tilt.data < -0.7 else self.left_tilt.data
            self.left_tilt_pub.publish(self.left_tilt)

        elif self.Joy.axes[7]<0 and self.count==0:
            self.left_tilt.data +=0.02
            self.left_tilt.data = 0.7 if self.left_tilt.data > 0.7 else self.left_tilt.data
            self.left_tilt_pub.publish(self.left_tilt)

        if self.Joy.axes[6]<0 and self.count==0:
            self.left_pan.data -=0.02
            self.left_pan.data = -0.7 if self.left_pan.data < -0.7 else self.left_pan.data
            self.left_pan_pub.publish(self.left_pan)

        elif self.Joy.axes[6]>0 and self.count==0:
            self.left_pan.data +=0.02
            self.left_pan.data = 0.7 if self.left_pan.data > 0.7 else self.left_pan.data
            self.left_pan_pub.publish(self.left_pan)
        
        ### mid camera 
        if self.Joy.axes[7]>0 and self.count==1:
            self.mid_tilt.data -=0.02
            self.mid_tilt.data = -0.7 if self.mid_tilt.data < -0.7 else self.mid_tilt.data
            self.mid_tilt_pub.publish(self.mid_tilt)

        elif self.Joy.axes[7]<0 and self.count==1:
            self.mid_tilt.data +=0.02
            self.mid_tilt.data = 0.7 if self.mid_tilt.data > 0.7 else self.mid_tilt.data
            self.mid_tilt_pub.publish(self.mid_tilt)

        if self.Joy.axes[6]<0 and self.count==1:
            self.mid_pan.data -=0.02
            self.mid_pan.data = -0.7 if self.mid_pan.data < -0.7 else self.mid_pan.data
            self.mid_pan_pub.publish(self.mid_pan)

        elif self.Joy.axes[6]>0 and self.count==1:
            self.mid_pan.data +=0.02
            self.mid_pan.data = 0.7 if self.mid_pan.data > 0.7 else self.mid_pan.data
            self.mid_pan_pub.publish(self.mid_pan)

        ### right camera 
        if self.Joy.axes[7]>0 and self.count==2:
            self.right_tilt.data -=0.02
            self.right_tilt.data = -0.7 if self.right_tilt.data < -0.7 else self.right_tilt.data
            self.right_tilt_pub.publish(self.right_tilt)

        elif self.Joy.axes[7]<0 and self.count==2:
            self.right_tilt.data +=0.02
            self.right_tilt.data = 0.7 if self.right_tilt.data > 0.7 else self.right_tilt.data
            self.right_tilt_pub.publish(self.right_tilt)

        if self.Joy.axes[6]<0 and self.count==2:
            self.right_pan.data -=0.02
            self.right_pan.data = -0.7 if self.right_pan.data < -0.7 else self.right_pan.data
            self.right_pan_pub.publish(self.right_pan)

        elif self.Joy.axes[6]>0 and self.count==2:
            self.right_pan.data +=0.02
            self.right_pan.data = 0.7 if self.right_pan.data > 0.7 else self.right_pan.data
            self.right_pan_pub.publish(self.right_pan)

if __name__ == "__main__":
    rospy.init_node("joy_mapper", anonymous=False)
    joy_mapper = Joymapper()
    rospy.spin()
