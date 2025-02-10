import rclpy
from action_msgs.msg import GoalStatus
from action_msgs.msg import GoalStatusArray
import sys

past_status = 0
goalPublisher = None
working = True
def feedbackCallback(msg:GoalStatusArray):
    global past_status
    global goalPublisher
    global working
    status = msg.status_list[-1].status
    if past_status != 4 and past_status != 0:
        if status == 4:
            print("done")
            #working = False
            #rclpy.shutdown()
            #goalPublisher.destroy_node()
            #rclpy.shutdown()
            sys.exit(1)
    if status == 5 or status == 6:
        print("error")
        sys.exit(2)
    past_status = status

rclpy.init()
goalPublisher = rclpy.create_node(f"myGoalChecker")
subscription = goalPublisher.create_subscription(GoalStatusArray, '/follow_path/_action/status', feedbackCallback, 10)

rclpy.spin(goalPublisher)
rclpy.shutdown()