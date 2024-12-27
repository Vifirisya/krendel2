import os
import sys
from geometry_msgs.msg import PoseStamped
from rclpy.duration import Duration
import rclpy

sys.path.insert(0, os.path.realpath(__file__).replace(f"scripts/krendel2.py", "launcher"))

import points
from robot_navigator import *

rclpy.init()
navigator = BasicNavigator()
navigator.lifecycleStartup()
#navigator.waitUntilNav2Active()
navigator.changeMap(os.path.realpath(__file__).replace(f"scripts/krendel2.py", "launcher/map.yaml"))

def go(pointName):
    print("!SCRIPT! doing \"GO\" !SCRIPT!")

    p = points.readPoints()
    pos = p[pointName]
    #os.system(f"ros2 topic pub /goal_pose geometry_msgs/PoseStamped \"{{header: {{stamp: {{sec: 0}}, frame_id: \'map\'}}, pose: {{position: {{x: {pos[0]}, y: {pos[1]}, z: 0.0}}, orientation: {{w: 1.0}}}}}}\"")

    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose.pose.position.x = pos[0]
    goal_pose.pose.position.y = pos[1]
    goal_pose.pose.position.z = 0.0
    goal_pose.pose.orientation.x = 0.0
    goal_pose.pose.orientation.y = 0.0
    goal_pose.pose.orientation.z = 0.0
    goal_pose.pose.orientation.w = 1.0

    navigator.goToPose(goal_pose)

    i = 0
 
    # Keep doing stuff as long as the robot is moving towards the goal
    while not navigator.isNavComplete():
        ################################################
        #
        # Implement some code here for your application!
        #
        ################################################
    
        # Do something with the feedback
        i = i + 1
        feedback = navigator.getFeedback()
        if feedback and i % 5 == 0:
            print('Distance remaining: ' + '{:.2f}'.format(feedback.distance_remaining) + ' meters.')
    
        # Some navigation timeout to demo cancellation
        if Duration.from_msg(feedback.navigation_time) > Duration(seconds=600.0):
            navigator.cancelNav()
    
        # Some navigation request change to demo preemption
        if Duration.from_msg(feedback.navigation_time) > Duration(seconds=120.0):
            goal_pose.pose.position.x = -3.0
            navigator.goToPose(goal_pose)
    
    # Do something depending on the return code
    result = navigator.getResult()
    if result == NavigationResult.SUCCEEDED:
        print('\nGoal succeeded!\n')
    elif result == NavigationResult.CANCELED:
        print('\nGoal was canceled!\n')
    elif result == NavigationResult.FAILED:
        print('\nGoal failed!\n')
    else:
        print('\nGoal has an invalid return status!\n')