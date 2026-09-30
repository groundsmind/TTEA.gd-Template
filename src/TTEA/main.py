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

            msg = client.poll()
            if msg is None:
                continue
            print(f"Received: {msg}")
            match msg:
                case "CAL":
                    pose_ctrl.calibrate()
                case "EXT":
                    break
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        client.close()