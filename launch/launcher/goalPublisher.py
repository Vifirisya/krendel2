import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped


class GoalPublisher(Node):

    def __init__(self, pos):
        super().__init__('goalPublisher')
        self.pos = pos
        self.publisher_ = self.create_publisher(PoseStamped, '/goal_pose', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = PoseStamped()
        msg.data = 'Hello World: %d' % self.i

        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = self.get_clock().now().to_msg()
        goal_pose.pose.position.x = self.pos[0]
        goal_pose.pose.position.y = self.pos[1]
        goal_pose.pose.position.z = 0.0
        goal_pose.pose.orientation.x = 0.0
        goal_pose.pose.orientation.y = 0.0
        goal_pose.pose.orientation.z = 0.0
        goal_pose.pose.orientation.w = 1.0

        self.publisher_.publish(goal_pose)