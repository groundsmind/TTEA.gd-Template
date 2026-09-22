from control import Control
from comm import InfoSender

if __name__ == "__main__":
    import sys

    sender = InfoSender()
    pose_ctrl = Control()

    sender.save_sock_info()

    addr = sender.get_endpoint_addr()
    arg = None

    while True:
        feet_pos = {'left': (0,0), 'right': (0,0)}
        feet_pos['left'], feet_pos['right'] = pose_ctrl.track()
        sender.send(feet_pos, addr)
        arg = sender.receive()
        if not arg:
            continue
        msg = arg["value"]
        match msg:
            case "CAL":
                pose_ctrl.calibrate()
            case "EXT":
                break