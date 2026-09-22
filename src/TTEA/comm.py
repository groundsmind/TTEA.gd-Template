import socket
import json

class InfoSender:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', 0))
        self.addr = socket.gethostbyname(socket.gethostname())
        _, self.port = self.sock.getsockname()
        print(f"Server started in UDP {self.addr}:{self.port}")

    def get_endpoint_addr(self):
        print("waiting for endpoint SYN...")
        data, addr = self.sock.recvfrom(1024)
        print(addr)
        message = json.loads(data.decode('utf-8'))
        if message['value'] != "SYN":
            addr = self.get_endpoint_addr()
            return addr
        print(f"Received {message['value']} from endpoint")
        #     TODO      #
	    # work this out #
        print(f"sending ACK...")
        self.sock.sendto(json.dumps("ACK").encode('utf-8'), addr)
        return addr

    def get_free_tcp_port(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as q_soc:
            q_soc.bind(('', 0))
            addr, port = q_soc.getsockname()
            q_soc.close()
            print(f"got free port {port}")
            return port

    def get_free_tcp_address(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as q_soc:
            q_soc.bind(('', 0))
            host, port = q_soc.getsockname()
            q_soc.close()
            print(f"got free address {host}")
            return '{host}'.format(**locals())

    def save_sock_info(self):
        with open("sockets.txt", "w") as f:
            f.write(f"{self.addr}:{self.port}")

    def receive(self):
        data = self.sock.recvfrom(1024)
        print(f"Got data: {data}")
        if data:
            message = json.loads(data[0].decode('utf-8'))
            return message
        return None

    def send(self, data, addr):
        self.sock.sendto(json.dumps(data).encode('utf-8'), addr)