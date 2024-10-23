import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import socket
import time
from threading import Thread
import os

cmd_value = {"linear" : 0, "angular" : 0}
ip = ""
with open(os.path.realpath(__file__).replace(f"/twistPublisher.py", "") + "/ip.txt", "r") as f:
    ip = f.read()
port = 2001

lastCall = time.time()
maxSilenceTime = 3

class TwistPublisher(Node):
    running = True
    def __init__(self):
        super().__init__("twist_publisher")
        self.publisher_ = self.create_publisher(Twist, "diff_drive_controller/cmd_vel_unstamped", 10)
        self.timer_ = self.create_timer(1.0/5.0, self.publish)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((ip, port))

        #self.listenThread = Thread(target=self.listen)
        #self.listenThread.start()

    def publish(self):
        global lastCall, cmd_value
        cmd_vel_manual = Twist()

        data, address = self.s.recvfrom(2048)
        data = data.decode("UTF-8")

        if data:
            try:
                linear = float(data.split(';')[0])
                angular = float(data.split(';')[1])
                #cmd_value["linear"] = linear
                #cmd_value["angular"] = angular

                cmd_vel_manual.linear.x = float(linear)
                cmd_vel_manual.angular.z = float(angular)

                self.publisher_.publish(cmd_vel_manual)

                #lastCall = time.time()
            except Exception:
                pass # pretend nothing happend

        #if time.time() - lastCall <= maxSilenceTime:
        #   cmd_vel_manual.linear.x = float(cmd_value["linear"])
        #   cmd_vel_manual.angular.z = float(cmd_value["angular"])
        #else:
        #    cmd_vel_manual.linear.x = 0.0
        #    cmd_vel_manual.angular.z = 0.0

        #self.publisher_.publish(cmd_vel_manual)

    def listen(self):
        global lastCall, cmd_value
        while self.running:
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

    def stop(self):
        self.running = False
        self.listenThread.join()

node = None
def start(args=None):
    global node
    rclpy.init(args=args)
    try:
        node = TwistPublisher()
        rclpy.spin(node)
        rclpy.shutdown()
    finally:
        #node.stop()
        pass

start()