import time

from camera import Camera
from pose_tracking import PoseTracking
from calibration import calibrar_ttea

class Control():
    def __init__(self):
        self.pose_tracking = PoseTracking()
        self.cap = None

    def calibrate(self, skip=False):
        if not skip:
            calibrar_ttea()
            time.sleep(0.3)
        self.cap = Camera()

    def get_feet_position(self):
        frame = self.cap.raw_frame if self.cap is not None else None
        if frame is not None:
            processed_frame = self.pose_tracking.scan_feets(frame)
            self.current_frame = processed_frame
        else:
            print("Câmera indisponível")

    
    def process_image(self):
        if self.cap is None:
            print("Câmera indisponível")
            return ((None, None), (None, None))
        self.cap.load_camera()
        self.get_feet_position()
        self.cap.display_camera()
        left_foot_x, left_foot_y = self.pose_tracking.get_left_foot()
        right_foot_x, right_foot_y = self.pose_tracking.get_right_foot()
        return((left_foot_x, left_foot_y), (right_foot_x, right_foot_y))

if __name__ == "__main__":
    import sys
    skip_calibration = "--skip-calibration" in sys.argv

    ctrl = Control()
    ctrl.calibrate(skip=skip_calibration)
    while True:
        print(ctrl.process_image())