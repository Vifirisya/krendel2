import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import socket
import time
from threading import Thread

cmd_value = {"linear" : 0, "angular" : 0}
ip = "192.168.50.217"
port = 2001

lastCall = time.time()
maxSilenceTime = 3

class TwistPublisher(Node):
    def __init__(self):
        super().__init__("twist_publisher")
        self.publisher_ = self.create_publisher(Twist, "cmd_vel_manual", 10)
        self.timer_ = self.create_timer(1.0/5.0, self.publish)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((ip, port))

        self.listenThread = Thread(target=self.listen)
        self.listenThread.start()

    def publish(self):
        cmd_vel_manual = Twist()

        if time.time() - lastCall <= maxSilenceTime:
            cmd_vel_manual.linear.x = float(cmd_value["linear"])
            cmd_vel_manual.angular.z = float(cmd_value["angular"])
        else:
            cmd_vel_manual.linear.x = 0.0
            cmd_vel_manual.angular.z = 0.0

        self.publisher_.publish(cmd_vel_manual)

    def listen(self):
        global lastCall, cmd_value
        while True:
            data, address = self.s.recvfrom(2048)
            data = data.decode("UTF-8")

            if data:
                try:
                    linear = float(data.split(';')[0])
                    angular = float(data.split(';')[1])
                    cmd_value["linear"] = linear
                    cmd_value["angular"] = angular

                    lastCall = time.time()
                except Exception:
                    pass # pretend nothing happend

def start(args=None):
    rclpy.init(args=args)
    node = TwistPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

start()