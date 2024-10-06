import socket
from threading import Thread

def inform(message):
    print(f"!COMMUNICATION! {message} !COMMUNICATION!")

class Communication:
    def __init__(self, ip, port):
        self.worklist = {}
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        inform(f"Binding on {ip}:{port}")
        self.s.bind((ip, port))

        inform("Starting listening")
        self.listenThread = Thread(target=self.listen)
        self.listenThread.start()
        
    def listen(self):
        while True:
            data, address = self.s.recvfrom(2048)
            data = data.decode("UTF-8")
            inform(f"{address} sent \"{data}\"")

            self.worklist[data[0]](data)

    def simplySend(self, data, address):
        self.s.sendto(bytes(data, "UTF-8"), address)
