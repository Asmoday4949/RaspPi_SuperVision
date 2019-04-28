import cv2
import imutils
import time
from .Camera import *

class MotionDetector:
    def __init__(self, min_threshold = 15, max_threshold = 255, blur_matrix_size = (9, 9)):
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold
        self.blur_matrix_size = blur_matrix_size
        self.last_frame = None

    def process(self, current_frame):
        detection = False
        last_frame = self.last_frame
        # Tranformations
        #current_frame = cv2.resize(current_frame, width=500)
        gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, self.blur_matrix_size, 0)

        # Get the very first image and pass the first iteration
        if last_frame is None:
            last_frame = gray
        else:
            # Get difference between two images and then try to determine the threshold
            frameDelta = cv2.absdiff(last_frame, gray)
            threshold = cv2.threshold(frameDelta, self.min_threshold, self.max_threshold, cv2.THRESH_BINARY)[1]

        	# dilate the thresholded image to fill in holes, then find contours
        	# on thresholded image
            thresh = cv2.dilate(threshold, None, iterations=2)
            contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)

            for contour in contours:
                if cv2.contourArea(contour) < 5000:
                    continue
            	# compute the bounding box for the contour, draw it on the frame,
            	# and update the text
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(current_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                detection = True
            last_frame = gray
        self.last_frame = last_frame
        return detection, current_frame

    def convert_jpeg(self, current_frame):
        return cv2.imencode('.jpg', current_frame)[1].tobytes()

    def process_and_convert_jpeg(self, current_frame):
        current_frame = self.process(current_frame)
        return convert_jpeg(current_frame)

def execute_test():
    ''' Launch test : check if MotionDetector work as expected '''
    camera = WebCamera()
    motion_detector = MotionDetector()
    last_frame = None
    while True:
        current_frame = camera.get_frame()[1]
        processed_frame = motion_detector.process(current_frame)

        cv2.imshow("Processed frame", processed_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
        	break
    cv2.destroyAllWindows()
    camera.stop()

if __name__ == "__main__":
    execute_test()
