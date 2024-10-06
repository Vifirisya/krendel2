from launcher import Process, Launcher
from communication import Communication

IP = "192.168.50.217"
PORT = 2000

PACKAGE_NAME = "krendel2"
LAUNCH_FILES = [Process("robot", "launch_robot.launch.py"),
                Process("lidar", "lidar.launch.py"),
                Process("slam", "slam_toolbox.launch.py"),
                Process("navigation", "nav2.launch.py"),
                Process("tp", "src/krendel2/launch/launcher/twistPublisher.py")]

launcher = Launcher(PACKAGE_NAME)
for process in LAUNCH_FILES:
    launcher.add(process)

launcher.runpy("tp")

def launch(data=None):
    file_keys = {'l': "lidar",
                'r':"robot",
                's':"slam",
                'n':"navigation"}
    if data:
        print(data)
        launcher.launch(file_keys[data.split(':')[1]])

def kill(data=None):
    file_keys = {'l': "lidar",
                'r':"robot",
                's':"slam",
                'n':"navigation"}
    if data:
        print(data)
        launcher.stop(file_keys[data.split(':')[1]])

def speed(data=None):
    if data:
        linear = float(data.split('l')[1].split('a')[0])
        angular = float(data.split('a')[1])
        communication.simplySend(f"{linear};{angular}", (IP, 2001))

def go(data=None):
    pass

worklist = {'l':launch,
            's':speed,
            'k':kill,
            'g':go,}

communication = Communication(IP, PORT)
communication.worklist = worklist
#launcher.finish()