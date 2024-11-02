import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import socket
import time
#import multiprocessing
import os
from threading import Thread

ip = ""
with open(os.path.realpath(__file__).replace(f"/twistPublisher.py", "") + "/ip.txt", "r") as f:
    ip = f.read()
port = 2001

lastCall = time.time()
maxSilenceTime = 1
class TwistPublisher(Node):
    running = True
    def __init__(self):
        super().__init__("twist_publisher")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.TCPServer.allow_reuse_address = True
        self.s.bind((ip, port))

        #self.listenThread = multiprocessing.Process(target=self.listen, args=())
        #self.listenThread.start()
        self.listenThread = Thread(target=self.listen)
        self.listenThread.start()
        self.publisher_ = self.create_publisher(Twist, "diff_drive_controller/cmd_vel_unstamped", 10)
        #self.publisher_ = self.create_publisher(Twist, "/wow", 10)
        self.timer_ = self.create_timer(1.0/5.0, self.publish)
        self.cmd_value = (0.0, 0.0)

    def publish(self):
        global maxSilenceTime
        global lastCall
        #print("publish ", self.cmd_value)
        cmd_vel_manual = Twist()

        if time.time() - lastCall <= maxSilenceTime:
        #cmd_value = (2.0, 2.0)
            cmd_vel_manual.linear.x = self.cmd_value[0]
            cmd_vel_manual.angular.z = self.cmd_value[1]
        #print("222", cmd_value)

        #cmd_vel_manual.linear.x = float("1.0")
        #cmd_vel_manual.angular.z = float("2.0")
        else:
            cmd_vel_manual.linear.x = 0.0
            cmd_vel_manual.angular.z = 0.0
        
        self.publisher_.publish(cmd_vel_manual)

    def listen(self):
        global lastCall
    
        while self.running:
            try:
                data, address = self.s.recvfrom(2048)
                data = data.decode("UTF-8")

                if data:
                
                    linear = float(data.split(';')[0])
                    angular = float(data.split(';')[1])
                    
                    self.cmd_value = (linear, angular)
                    #self.cmd_value["linear"] = linear
                    #self.cmd_value["angular"] = angular

                    lastCall = time.time()
            except KeyboardInterrupt:
                print("ctrl c")
                self.stop()
                break
            #print("listen", self.cmd_value)
            #self.publish()

        print("im finally done!!!!!!!")
        exit()
    def stop(self):
        try:
            print("trying to stop this idiot")
            self.running = False
            self.s.close()
        except KeyboardInterrupt:
            print("let me stop!!!")
            self.running = False
            self.s.close()
        #self.listenThread.terminate()
        #time.sleep(2)

node = None
def start(args=None):
    global node
    rclpy.init(args=args)
    try:
        node = TwistPublisher()
        rclpy.spin(node)
    finally:
        node.stop()
        #time.sleep(2)
        try:
            rclpy.shutdown()
            node.stop()
        finally:
            exit()

start()