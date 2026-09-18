from control import Control
from comm import InfoSender

if __name__ == "__main__":
    sender = InfoSender()
    ctrl = Control()

    addr = sender.get_endpoint_addr()
    