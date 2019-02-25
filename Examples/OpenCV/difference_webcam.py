import cv2 as ocv
import numpy as npy

def readCamera():
    print ("q to quit")
    cap = ocv.VideoCapture(0)

    # Read the first frame
    ret, lastFrame = cap.read()
    lastGreyFrame = ocv.cvtColor(lastFrame, ocv.COLOR_BGR2GRAY)
    output = npy.zeros((lastFrame.shape[0],lastFrame.shape[1],1), npy.uint8)
    i = 0
    while(True):
        # Capture frame-by-frame
        ret, currentFrame = cap.read()

        # Convert to grey scale
        currentGreyFrame = ocv.cvtColor(currentFrame, ocv.COLOR_BGR2GRAY)

        # Substract
        output = ocv.subtract(lastGreyFrame, currentGreyFrame)

        # Indicate that a movement has been detected
        diff = npy.where(output > 80);
        if(len(diff[0]) > 0):
            print("Movement detected")

        # Display the resulting frame
        ocv.imshow('camera', output)
        if ocv.waitKey(1) & 0xFF == ord('q'):
            break
        # Save the last frame
        lastGreyFrame = currentGreyFrame
    cap.release()
    ocv.destroyAllWindows()

if __name__ == "__main__":
    readCamera()
