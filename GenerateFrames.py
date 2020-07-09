from cv2 import cv2
import sys

#print(sys.argv[1])

vidcap = cv2.VideoCapture('./Movie-Trailers/' + sys.argv[1] + '.avi')

def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite("./Movie-Trailers/" + sys.argv[1] + "/image"+str(count)+".jpg", image)     # save frame as JPG file
    return hasFrames

sec = 0
frameRate = 0.5     #//it will capture an image each 0.5 seconds
count=1
success = getFrame(sec)

while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)