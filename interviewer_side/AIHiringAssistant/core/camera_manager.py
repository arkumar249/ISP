import cv2

class CameraManager:
    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)

        # Set thermal camera resolution only if using a live camera (int source)
        if isinstance(source, int):
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 192)

    def read(self):
        if self.cap.isOpened():
            return self.cap.read()
        return False, None

    def release(self):
        if self.cap.isOpened():
            self.cap.release()
