import subprocess
import time
#from ament_index_python.packages import get_package_share_directory

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

    def launch(self, name):
        inform(f"Launching \"{name}\"")
        filename = self.processes[name].filename
        self.processes[name].process = subprocess.Popen(["ros2", "launch", self.packageName, filename])
        self.processes[name].running = True

    def run(self, name):
        inform(f"Running \"{name}\"")
        filename = self.processes[name].filename
        self.processes[name].process = subprocess.Popen(["ros2", "run", self.packageName, filename])
        self.processes[name].running = True
        
    def runpy(self, name):
        inform(f"Running \"{name}\"")
        filename = self.processes[name].filename
        self.processes[name].process = subprocess.Popen(["python3", filename])
        self.processes[name].running = True

    def runpy(self, name):
        inform(f"Running \"{name}\"")
        filename = self.processes[name].filename
        self.processes[name].process = subprocess.Popen(["python3", filename])
        self.processes[name].running = True

    def stop(self, name:str):
        while self.processes[name].ping():
            inform(f"Killing \"{name}\"")
            try:
                self.processes[name].process.terminate()
                self.processes[name].running = False
            except AttributeError:
                inform(f"Unable to kill \"{name}\"")
                self.processes[name].running = False

        self.processes[name].process = None
        #self.processes[name].process = False

    def ping(self):
        for name, process in self.processes.items():
            process.ping(True)

    def finish(self):
        for name, process in self.processes.items():
            if process != None:
                self.stop(name)

    def remove(self, name):
        del self.processes[name]