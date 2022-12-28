#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped 
from geometry_msgs.msg import Pose
import math
import time
from std_srvs.srv import Empty
from std_msgs.msg import Empty
empty_msg = Empty()
twist_msg = Twist()
#desired_pose.header.frame_id='world'
x=0
y=0
z=0
def poseCallback(pose_message):
    global x
    global y, z
    x= pose_message.pose.position.x
    y= pose_message.pose.position.y
    z= pose_message.pose.position.z
   # print ('x','y'.'z')
    


def movexp(): 
  twist_msg = Twist()
  #twist_msg.header.frame_id='world'
  twist_msg.linear.x= 1
  #i = 0
  while x < 1:
      cmd_vel_pub.publish(twist_msg)
      #i = i + 1
      rate.sleep()
  
  twist_msg.linear.x= 0
  cmd_vel_pub.publish(twist_msg)

def movexn(): 
  twist_msg = Twist()
  #twist_msg.header.frame_id='world'
  twist_msg.linear.x= -1
  #i = 0
  while x > -1:
      cmd_vel_pub.publish(twist_msg)
      #i = i + 1
      rate.sleep()
  
  twist_msg.linear.x= 0
  cmd_vel_pub.publish(twist_msg)

def movey(): 
  twist_msg = Twist()
  #twist_msg.header.frame_id='world'
  twist_msg.linear.y=2
  #i = 0
  while y < 1:
      cmd_vel_pub.publish(twist_msg)
      #i = i + 1
      rate.sleep()
  
  twist_msg.linear.y= 0
  cmd_vel_pub.publish(twist_msg)
  
def moveyy(): 
  twist_msg = Twist()
  #twist_msg.header.frame_id='world'
  twist_msg.linear.y=2
  #i = 0
  while y < 2:
      cmd_vel_pub.publish(twist_msg)
      #i = i + 1
      rate.sleep()
  
  twist_msg.linear.y= 0
  cmd_vel_pub.publish(twist_msg)
def takeoff(): 
  twist_msg = Twist()
  twist_msg.linear.z = 0.4
  i = 0
  while i < 3:
      cmd_vel_pub.publish(twist_msg)
      i = i + 1
      rate.sleep()
  
  twist_msg.linear.z = 0
  cmd_vel_pub.publish(twist_msg)
  
def land():
  twist_msg = Twist() 
  twist_msg.linear.z = -0.5
  i = 0
  while i < 10:
      cmd_vel_pub.publish(twist_msg)
      i = i + 1
      rate.sleep()
  
  twist_msg.linear.z = 0
  cmd_vel_pub.publish(twist_msg)
  
def go_to_goal( x_now, y_now):
    global x
    global y, z
    x_goal=2
    y_goal=2
    #desired_pose.header.frame_id='world'
    velocity_message =Twist()

    while (True):
        K_linear = 0.5 
        distance = abs(math.sqrt(((x_goal-x_now) ** 2) + ((y_goal-y_now) ** 2)))

        linear_speed = distance * K_linear

        K_angular = 4.0
        desired_angle_goal = math.atan2(y_goal-y_now, x_goal-x_now)
       # angular_speed = (desired_angle_goal-yaw)*K_angular

        velocity_message.linear.x = linear_speed
        #velocity_message.angular.z = angular_speed

        cmd_vel_pub.publish(velocity_message)
        print ('x=', x_now, ', y=',y_now, ', distance to goal: ', distance)

        if (distance <0.1):
            break

  
  
def dronemotion():
    global x
    global y, z
    vel_msg = Twist()
    desired_pose = PoseStamped()
    #desired_pose.header.frame_id='world'
    desired_pose.pose.position.x = 1
    desired_pose.pose.position.y = 1
    desired_pose.pose.position.z = 0
    loop_rate = rospy.Rate(1)
            
    takeoff()
    time.sleep(1)
    movexn()
    #go_to_goal(x,y)
    time.sleep(1)
    movey()
    time.sleep(1)
    movexp()
    time.sleep(1)
    movey()
    time.sleep(1)
    movexn()
    time.sleep(1)
    land()
    time.sleep(1)
    pass







if __name__ == '__main__':
    try:
    
        
        rospy.init_node('drone_motion_pose', anonymous=True)
        rate=rospy.Rate(1)
        cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        position_topic = "/ground_truth_to_tf/pose"
        pose_subscriber = rospy.Subscriber(position_topic,PoseStamped, poseCallback) 
        time.sleep(2)

        
        rospy.loginfo("start movement")
        dronemotion()
        empty_msg = Empty()
        twist_msg = Twist()
        rospy.spin()
        
       
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")
