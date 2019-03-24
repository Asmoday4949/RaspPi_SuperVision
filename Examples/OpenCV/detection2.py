# import the necessary packages
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

# Get the main video capture of the system
video_stream = cv2.VideoCapture(0)

# Prepare variable for the first frame
last_frame = None

# Variable to indicate that we stream
stream = True

# Main loop
while stream:
    result, frame = video_stream.read()

    # Check if we get the image
    if frame is None:
        break

    # Tranformations
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9, 9), 0)

    # Get the very first image and pass the first iteration
    if last_frame is None:
        last_frame = gray
        continue

    # Get difference between two images and then try to determine the threshold
    frameDelta = cv2.absdiff(last_frame, gray)
    threshold = cv2.threshold(frameDelta, 15, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
    thresh = cv2.dilate(threshold, None, iterations=2)
    cnts = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
    	# compute the bounding box for the contour, draw it on the frame,
    	# and update the text
    	(x, y, w, h) = cv2.boundingRect(c)
    	cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    	text = "Occupied"

    # draw the text and timestamp on the frame
    #cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    #cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", threshold)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
    	break

    last_frame = gray

# cleanup the camera and close any open windows
video_stream.release()
cv2.destroyAllWindows()
