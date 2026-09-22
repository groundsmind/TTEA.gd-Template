from control import Control
from client import Client
from threading import Thread

if __name__ == "__main__":
    client = Client()
    pose_ctrl = Control()

    try:
        while True:
            feet_pos = {'left': (0,0), 'right': (0,0)}
            feet_pos['left'], feet_pos['right'] = pose_ctrl.track()
            client.send(feet_pos)

            arg = None
            arg = client.receive()
            if not arg:
                continue
            msg = arg
            match msg:
                case "CAL":
                    pose_ctrl.calibrate()
                    client.send("CAL_OK")
                case "EXT":
                    break
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        client.close()