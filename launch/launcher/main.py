from launcher import Process, Launcher
from communication import Communication, myIP
import os
import threading
import time
from points import *
import glob

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
                Process("tp", "src/krendel2/launch/launcher/twistPublisher.py"),
                Process("mp", "src/krendel2/launch/launcher/mapPublisher.py"),
                Process("script", "src/krendel2/launch/scripts/main.py")]

launcher = Launcher(PACKAGE_NAME)
for process in LAUNCH_FILES:
    launcher.add(process)

launcher.runpy("mp")

def launch(data=None):
    file_keys ={'l':"lidar",
                'r':"robot",
                's':"slam",
                'n':"navigation"}
    if data:
        print(data)
        launcher.launch(file_keys[data.split(':')[1]])

def kill(data=None):
    file_keys = {'l':"lidar",
                'r':"robot",
                's':"slam",
                'n':"navigation",
                't':"tp"}
    if data:
        print(data)
        launcher.stop(file_keys[data.split(':')[1]])

def close(data=None):
    #os.popen("sudo -S %s"%("shutdown now"), 'w').write('123456\n')
    #subprocess.run(['sudo', "shutdown now"], input="123456".encode())
    os.system("sudo shutdown now")
    

def reload(data=None):
    os.system("sudo systemctl reboot")

lastSpeedSend = 0
speedSendT = 0.2
def speed(data=None):
    global lastSpeedSend
    global speedSendT
    if data and ((time.time() - lastSpeedSend) >= speedSendT):
        linear = float(data.split('l')[1].split('a')[0])
        angular = float(data.split('a')[1])
        lastSpeedSend = time.time()
        communication.simplySend(f"{linear};{angular}", (IP, 2001))

def go(data=None):
    global launcher
    if launcher.processes["script"].running:
        launcher.stop("script")
    launcher.runpy("script")

def runTwistPublisher(data=None):
    launcher.runpy("tp")

def eraseMap(data=None):
    try:
        os.remove(os.path.realpath(__file__).replace(f"/main.py", "/map.data"))
        os.remove(os.path.realpath(__file__).replace(f"/main.py", "/map.posegraph"))
        print("The map is erased")
    except FileNotFoundError:
        print>("The map has already been erased")

worklist = {'l':launch,
            's':speed,
            'k':kill,
            'g':go,
            'c':close,
            'r':reload,
            'p':newPoint,
            'd':deletePoint,
            't':runTwistPublisher,
            'e':eraseMap}

print(myIP())
communication = Communication(IP, PORT)
communication.worklist = worklist

overseering = True
def overseer(T):
    global IP
    global launcher
    global communication
    global overseering

    file_keys ={'l': "lidar",
                'r':"robot",
                's':"slam",
                'n':"navigation",
                't':"tp"}
    while overseering:
        totalStatus = launcher.status()

        for letter in file_keys:
            process = file_keys[letter]
            status = totalStatus[process]
            
            message = "s:" + letter + ':' + str(int(status))
            communication.simplySend(message, (IP, 2002))

        # list_of_files = glob.glob('/home/timofey/.ros/log/controller_server*.log') # * means all if need specific format then *.csv
        # filename = max(list_of_files, key=os.path.getctime)
        # output = ""
        # fullname = os.path.join("/home/timofey/.ros/log/", filename)
        # #print(fullname)

        # if launcher.processes['navigation'].process != None:
        #     #output = launcher.processes['navigation'].readLine()
            
        #     with open(fullname, "r") as f:
        #         try:
        #             output = f.read().split('\n')[-2]
        #         except IndexError:
        #             #print("")
        #             pass
        #     if output:
        #         #print("navigation: ", end="")
        #         #print(output, end="\n")
        #         communication.simplySend(output, (IP, 2004))
        #communication.simplySend("yo", (IP, 2004))

        #time.sleep(T)

overseerThread = threading.Thread(target=overseer, args=(0.3,))
overseerThread.start()

while True:
    try:
        communication.listen()
    except KeyboardInterrupt:
        print("\nSafe stop\n")
        overseering = False
        overseerThread.join()
        time.sleep(2)
        break
    finally:
        pass

launcher.finish()