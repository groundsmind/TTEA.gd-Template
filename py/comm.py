import socket
import json

class InfoSender:
    def __init__(self):
        # Setup a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("127.0.0.1", 4242))

    def get_endpoint_addr(self):
        print("waiting for endpoint ack...")
        data, addr = self.sock.recvfrom(1024)
        message = json.loads(data.decode('utf-8'))
        print(f"Received from Godot: {message}")
        return addr
        response = {"status": "success", "result": message.get("value", 0) * 2}
            

    def send(self, data, addr):
        self.sock.sendto(json.dumps(data).encode('utf-8'), addr)