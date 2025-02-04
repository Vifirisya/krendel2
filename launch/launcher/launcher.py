import subprocess
import time
from ament_index_python.packages import get_package_share_directory

def inform(message):
    print(f"!LAUNCHER! {message} !LAUNCHER!")

class Process:
    def __init__(self, name, filename, process=None) -> None:
        self.name = name
        self.filename = filename
        self.process = process

        if(self.process): self.running = True
        else: self.running = False

    def ping(self, info=False):
        if self.process:
            if self.process.poll() is not None:
                if info:
                    inform(f"Process \"{self.name}\" is dead")
                return False
            
            else:
                if info:
                    inform(f"Process \"{self.name}\" is ok")
                return True
        else:
            if info:
                inform(f"Process \"{self.name}\" is dead")
            return False

    def readLine(self):
        try:
            return next(iter(self.process.stdout.readline))
        finally: 
            return ""

    def content(self):
        return {"filename": self.filename, "process": self.process, "running":self.running}

class Launcher:
    def __init__(self, packageName:str):
        self.processes = {}
        self.packageName = packageName

    def add(self, name:str, filename:str):
        self.processes[name] = Process(name, filename)

    def add(self, process:Process):
        self.processes[process.name] = process

    # Launch ROS package
    def launch(self, name):
        inform(f"Launching \"{name}\"") # Indicate launching
        filename = self.processes[name].filename # Get filename from process list
        self.processes[name].process = subprocess.Popen(["ros2", "launch", self.packageName, filename], stdout=subprocess.PIPE, text=True) # Launch file
        self.processes[name].running = True # Set process as running

    def run(self, name):
        inform(f"Running \"{name}\"")  # Indicate running
        filename = self.processes[name].filename # Get filename from process list
        self.processes[name].process = subprocess.Popen(["ros2", "run", self.packageName, filename], stdout=subprocess.PIPE, text=True) # Run file
        self.processes[name].running = True # Set process as running
        
    def runpy(self, name):
        inform(f"Running \"{name}\"")  # Indicate running
        filename = self.processes[name].filename # Get filename from process list
        self.processes[name].process = subprocess.Popen(["python3", filename], stdout=subprocess.PIPE, text=True) # Run python file
        self.processes[name].running = True # Set process as running

    def stop(self, name:str):
        while self.processes[name].ping(): # Does not stop until process is stopped
            inform(f"Killing \"{name}\"")  # Indicate stopping
            try:
                self.processes[name].process.terminate() # Send stop signal
                self.processes[name].running = False # Set process as not running
            except AttributeError: # In case of failure
                inform(f"Unable to kill \"{name}\"") # Show error message
                self.processes[name].running = False # Set proces as not running (to notS use it again)

        self.processes[name].process = None # Delete process (to not use it again)

    def ping(self):
        for name, process in self.processes.items():
            process.ping(True)

    def status(self):
        status = {}
        for name, process in self.processes.items():
            if process.process is not None:
                if process.ping():
                    status[name] = True
                else:
                    status[name] = False
            else:
                status[name] = False
        return status

    def finish(self):
        for name, process in self.processes.items():
            if process != None:
                self.stop(name)

    def remove(self, name):
        del self.processes[name]