import os
import sys
from geometry_msgs.msg import PoseStamped
from rclpy.duration import Duration
import rclpy
import socket
import time
from nav2_msgs.action import NavigateToPose, FollowPath
from rclpy.action import ActionClient
from action_msgs.msg import GoalStatus
from std_msgs.msg import String
import subprocess
sys.path.insert(0, os.path.realpath(__file__).replace(f"scripts/krendel2.py", "launcher"))

import points
#from robot_navigator import *
#from goalPublisher import GoalPublisher

#navigator = BasicNavigator()
#navigator.lifecycleStartup()
#navigator.waitUntilNav2Active()
#navigator.changeMap(os.path.realpath(__file__).replace(f"scripts/krendel2.py", "launcher/map.yaml"))

iteration = 0
ip = ""
with open(os.path.realpath(__file__).replace(f"/scripts/krendel2.py", "/launcher/ip.txt"), "r") as f:
    ip = f.read()
port = 2004

def feedbackCallback(msg):
    print("aaaaaa  ", end="")
    print(msg)

def go(pointName):
    global iteration
    print("!SCRIPT! doing \"GO\" !SCRIPT!")

    p = points.readPoints()
    pos = p[pointName]
    #goalPublisher = GoalPublisher(pos)

    rclpy.init()

    goalPublisher = rclpy.create_node(f"goalPublisher_{iteration}")
    iteration += 1
    publisher = goalPublisher.create_publisher(PoseStamped, '/goal_pose', 10)
    #subscription = goalPublisher.create_subscription(String, '/follow_path/_action/status', feedbackCallback, 10)

    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = goalPublisher.get_clock().now().to_msg()
    goal_pose.pose.position.x = pos[0]
    goal_pose.pose.position.y = pos[1]
    goal_pose.pose.position.z = 0.0
    goal_pose.pose.orientation.x = 0.0
    goal_pose.pose.orientation.y = 0.0
    goal_pose.pose.orientation.z = 0.0
    goal_pose.pose.orientation.w = 1.0

    while publisher.get_subscription_count() < 1:
        time.sleep(0.1)
        print(f"\nWaiting for connection; {pointName}\n")
    publisher.publish(goal_pose)
    goalPublisher.destroy_node()
    rclpy.shutdown()
    process = subprocess.Popen(['python3', os.path.realpath(__file__).replace(f"krendel2.py", "goalChecker.py")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while process.poll() == None:
        time.sleep(1)
        print(f"Doing {pointName}")
    #stdout, stderr = process.communicate()
    print("!!!Important")
    print(process.returncode)
    print("!!!Important")

    if process.returncode == 0:
        print("Success!!!!!!!!!!")
    else:
        print("Error!!!!!!!!!")
        go(pointName)

    # print("!SCRIPT! doing \"GO\" !SCRIPT!")

    # p = points.readPoints()
    # pos = p[pointName]
    # #goalPublisher = GoalPublisher(pos)

    # rclpy.init()

    # goalPublisher = rclpy.create_node("goalPublisher")
    # publisher = goalPublisher.create_publisher(PoseStamped, '/goal_pose', 10)
    # #nav_to_pose_client = ActionClient(goalPublisher, NavigateToPose, 'navigate_to_pose')

    # goal_pose = PoseStamped()
    # goal_pose.header.frame_id = 'map'
    # goal_pose.header.stamp = goalPublisher.get_clock().now().to_msg()
    # goal_pose.pose.position.x = pos[0]
    # goal_pose.pose.position.y = pos[1]
    # goal_pose.pose.position.z = 0.0
    # goal_pose.pose.orientation.x = 0.0
    # goal_pose.pose.orientation.y = 0.0
    # goal_pose.pose.orientation.z = 0.0
    # goal_pose.pose.orientation.w = 1.0



    # publisher.publish(goal_pose)

    # send_goal_future = nav_to_pose_client.send_goal_async(goal_msg,
    #                                                             feedbackCallback)
    # rclpy.spin_until_future_complete(goalPublisher, send_goal_future)
    # goal_handle = send_goal_future.result()

    # if not goal_handle.accepted:
    #     print("not accepted :(((((((((((((")
    #     sys.exit()

    # print("\n\n\n\n done \n\n\n\n")

    # result_future = goal_handle.get_result_async()
    # if result_future:
    #     if result_future.result().status == GoalStatus.STATUS_SUCCEEDED:
    #         print("\n\nyoooooooo yes yeeeeeeeeeeees\n\n")
    #     else:
    #         print("\n\nnoooooooooooooooooooooooooo\n\n")

    # rclpy.shutdown()
    #rclpy.spin(goalPublisher)

    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # s.bind((ip, port))

    # finished = False
    # while not finished:
    #     #print("a")
    #     data, address = s.recvfrom(2048)
    #     #print("b")
    #     data = data.decode("UTF-8")

    #     if data:
    #         print(f"!SCRIPT! received \"{data}\" !SCRIPT!")
    #         if "Goal succeeded" in data or "Reached the goal!" in data:
    #             print("\n\nyeeeeeeeeeeeeeeeeeees\n\n")
    #             finished = True
    #             break
    #         elif "Failed to make progress" in data or "Aborting handle" in data:
    #             print("\n\nnooooooooooooooooo\n\n")
    #             sys.exit()

    #s.close()
    #rclpy.shutdown()
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