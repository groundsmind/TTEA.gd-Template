import socket
import json
import time
import threading
import queue
from pathlib import Path

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.ip, self.port = self.get_server_ip_port()
        self.port = int(self.port)
        self.addr = (self.ip, self.port)
        print(f"Server port: {self.port}")

        self.inbox = queue.Queue()
        self.running = threading.Event()
        self.running.set()
        self.thread = threading.Thread(target=self._listen, daemon=True)
        self.thread.start()

        self.connect()

    def get_server_ip_port(self):
        current_dir = Path(__file__).resolve().parent
        with open(current_dir / "sockdata.txt", "+r") as f:
            data = f.read()
            data = data.split(":")
        return data

    def connect(self):
        self.send("SYN")
        print("SYN sent, awaiting ACK...")

    def _listen(self):
        while self.running.is_set():
            try:
                data, (recv_ip, recv_port) = self.client.recvfrom(1024)
                message = data.decode('utf-8')
                print(f"Got data: {message}")
                return message
            except socket.timeout:
                continue
            except ConnectionResetError:
                print("Source not yet ready. retrying in a second")
                time.sleep(1)
            except OSError:
                break

    def poll(self):
        try:
            return self.inbox.get_nowait()
        except queue.Empty:
            return None

    def send(self, data):
        tosend = json.dumps(data).encode('utf-8')
        print(f"Sending: {tosend}")
        self.client.sendto(tosend, self.addr)

    def close(self):
        self.client.close()