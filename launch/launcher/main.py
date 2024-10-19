from launcher import Process, Launcher
from communication import Communication, myIP
import os
import subprocess

IP = myIP()
PORT = 2000

#print(os.path.realpath(__file__).replace(f"/main.py", "") + "/ip.txt")
with open(os.path.realpath(__file__).replace(f"/main.py", "") + "/ip.txt", "w") as f:
    f.write(IP)

PACKAGE_NAME = "krendel2"
LAUNCH_FILES = [Process("robot", "launch_robot.launch.py"),
                Process("lidar", "lidar.launch.py"),
                Process("slam", "slam_toolbox.launch.py"),
                Process("navigation", "nav2.launch.py"),
                Process("tp", "src/krendel2/launch/launcher/twistPublisher.py")]

launcher = Launcher(PACKAGE_NAME)
for process in LAUNCH_FILES:
    launcher.add(process)

#launcher.runpy("tp")

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

def close(data=None):
    #os.popen("sudo -S %s"%("shutdown now"), 'w').write('123456\n')

    subprocess.Popen('sudo -S' , shell=True,stdout=subprocess.PIPE)
    subprocess.Popen("123456" , shell=True,stdout=subprocess.PIPE)
    subprocess.Popen("sudo shutdown now" , shell=True,stdout=subprocess.PIPE)

def reload(data=None):
    #os.system("sudo systemctl reboot")
    #os.popen("sudo -S %s"%("systemctl reboot"), 'w').write('123456\n')

    subprocess.Popen('sudo -S' , shell=True,stdout=subprocess.PIPE)
    subprocess.Popen("123456" , shell=True,stdout=subprocess.PIPE)
    subprocess.Popen("sudo systemctl reboot" , shell=True,stdout=subprocess.PIPE)

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
            'g':go,
            'c':close,
            'r':reload}

print(myIP())
communication = Communication(IP, PORT)
communication.worklist = worklist

while True:
    try:
        communication.listen()
    except KeyboardInterrupt:
        print("\nSafe stop\n")
        break
    finally:
        #communication.stop()
        pass
    
#launcher.finish()