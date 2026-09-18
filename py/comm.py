import socket
import json

class InfoSender:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("127.0.0.1", 4242))

    def get_endpoint_addr(self):
        print("waiting for endpoint SYN...")
        data, addr = self.sock.recvfrom(1024)
        message = json.loads(data.decode('utf-8'))
        if message['value'] != "SYN":
            addr = self.get_endpoint_addr()
            return addr
        print(f"Received {message['value']} from endpoint")
        return addr

    def receive(self):
        data = self.sock.recvfrom(1024)
        message = json.loads(data.decode('utf-8'))
        return message

    def send(self, data, addr):
        self.sock.sendto(json.dumps(data).encode('utf-8'), addr)