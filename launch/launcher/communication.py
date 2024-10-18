import socket
from threading import Thread

def inform(message):
    print(f"!COMMUNICATION! {message} !COMMUNICATION!")

def myIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

class Communication:
    running = True
    def __init__(self, ip, port):
        self.worklist = {}
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        inform(f"Binding on {ip}:{port}")
        self.s.bind((ip, port))

        inform("Starting listening")
        self.listenThread = Thread(target=self.listen)
        self.listenThread.start()
        
    def listen(self):
        while self.running:
            data, address = self.s.recvfrom(2048)
            data = data.decode("UTF-8")
            inform(f"{address} sent \"{data}\"")

            self.worklist[data[0]](data)

    def simplySend(self, data, address):
        self.s.sendto(bytes(data, "UTF-8"), address)

    def stop(self):
        try:
            self.running = False
            self.listenThread.join()
        except KeyboardInterrupt:
            print("aa")
            self.running = False
            self.listenThread.join()
