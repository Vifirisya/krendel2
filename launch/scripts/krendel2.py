import os
import sys
from geometry_msgs.msg import PoseStamped
from rclpy.duration import Duration
import rclpy
import socket

sys.path.insert(0, os.path.realpath(__file__).replace(f"scripts/krendel2.py", "launcher"))

import points
#from robot_navigator import *
from goalPublisher import GoalPublisher

#navigator = BasicNavigator()
#navigator.lifecycleStartup()
#navigator.waitUntilNav2Active()
#navigator.changeMap(os.path.realpath(__file__).replace(f"scripts/krendel2.py", "launcher/map.yaml"))

ip = ""
with open(os.path.realpath(__file__).replace(f"/scripts/krendel2.py", "/launcher/ip.txt"), "r") as f:
    ip = f.read()
port = 2004

print(f"!SCRIPT! doing \"{ip}\" !SCRIPT!")

def go(pointName):
    print("!SCRIPT! doing \"GO\" !SCRIPT!")
    rclpy.init()

    p = points.readPoints()
    pos = p[pointName]
    goalPublisher = GoalPublisher(pos)

    #rclpy.spin(goalPublisher)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, port))

    finished = False
    while not finished:
        print("a")
        data, address = s.recvfrom(2048)
        print("b")
        data = data.decode("UTF-8")

        if data:
            print(f"!SCRIPT! received \"{data}\" !SCRIPT!")
            if "Goal succeeded" in data or "Reached the goal!" in data:
                print("\n\nyeeeeeeeeeeeeeeeeeees\n\n")
                finished = True
                break
            elif "Failed to make progress" in data or "Aborting handle" in data:
                print("\n\nnooooooooooooooooo\n\n")
                sys.exit()

    s.close()
    rclpy.shutdown()
    #os.system(f"ros2 topic pub /goal_pose geometry_msgs/PoseStamped \"{{header: {{stamp: {{sec: 0}}, frame_id: \'map\'}}, pose: {{position: {{x: {pos[0]}, y: {pos[1]}, z: 0.0}}, orientation: {{w: 1.0}}}}}}\"")

    # navigator.goToPose(goal_pose)

    # i = 0
 
    # # Keep doing stuff as long as the robot is moving towards the goal
    # while not navigator.isNavComplete():
    #     ################################################
    #     #
    #     # Implement some code here for your application!
    #     #
    #     ################################################
    
    #     # Do something with the feedback
    #     i = i + 1
    #     feedback = navigator.getFeedback()
    #     if feedback and i % 5 == 0:
    #         print('Distance remaining: ' + '{:.2f}'.format(feedback.distance_remaining) + ' meters.')
    
    #     # Some navigation timeout to demo cancellation
    #     if Duration.from_msg(feedback.navigation_time) > Duration(seconds=600.0):
    #         navigator.cancelNav()
    
    #     # Some navigation request change to demo preemption
    #     if Duration.from_msg(feedback.navigation_time) > Duration(seconds=120.0):
    #         goal_pose.pose.position.x = -3.0
    #         navigator.goToPose(goal_pose)
    
    # # Do something depending on the return code
    # result = navigator.getResult()
    # if result == NavigationResult.SUCCEEDED:
    #     print('\nGoal succeeded!\n')
    # elif result == NavigationResult.CANCELED:
    #     print('\nGoal was canceled!\n')
    # elif result == NavigationResult.FAILED:
    #     print('\nGoal failed!\n')
    # else:
    #     print('\nGoal has an invalid return status!\n')