import socket
import json

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.ip, self.port = self.get_server_ip_port()
        self.port = int(self.port)
        self.addr = (self.ip, self.port)
        print(f"Server port: {self.port}")
        self.connect()

    def get_server_ip_port(self):
        with open("sockdata.txt", "+r") as f:
            data = f.read()
            data = data.split(":")
        return data

    def connect(self):
        self.send("SYN")
        print("SYN sent, awaiting ACK...")

    def receive(self):
        data, (recv_ip, recv_port) = self.client.recvfrom(1024)
        message = data.decode('utf-8')
        print(f"Got data: {message}")
        return message

    def send(self, data):
        tosend = json.dumps(data).encode('utf-8')
        print(f"Sending: {tosend}")
        self.client.sendto(tosend, self.addr)

    def close(self):
        self.client.close()