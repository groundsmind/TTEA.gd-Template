from control import Control
from comm import InfoSender

if __name__ == "__main__":
    sender = InfoSender()
    pose_ctrl = Control()

    pose_ctrl.calibrate()
    addr = sender.get_endpoint_addr()

    while True:
        lfoot, rfoot = (0,0)
        lfoot, rfoot = pose_ctrl.track()
        sender.send((lfoot, rfoot), addr)