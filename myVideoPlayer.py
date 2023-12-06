#!/usr/bin/env python3
from ExtractAndDisplay import *
from myQueue import *
import sys

debug = None
if(len(sys.argv) > 2): debug = sys.argv[2]

def extractFrames(vidcap, outputBuffer, maxFramesToLoad=9999):
    # open video file, get frame count
    global frameCount 
    # read first image
    success,image = vidcap.read() 
    if debug: print(f'Reading frame {0} {success}')
    for i in range(frameCount):
        # get a jpg encoded frame
        success, jpgImage = cv2.imencode('.jpg', image)
        if success != True:
            print('Frame extraction Failure')
            return
        #encode the frame as base 64 to make debugging easier
        jpgAsText = base64.b64encode(jpgImage)
        # add the frame to the buffer
        outputBuffer.put(image)
        success,image = vidcap.read()
        if debug: print(f'Reading frame {i} {success}')
    print('Frame extraction complete')

#take frames from inBuffer, convert to grayscale, put them in outBuffer 
def convertToGrayScale(inBuffer: myQueue, outBuffer: myQueue):
    inputFrame = inBuffer.get() #consume next frame
    global frameCount
    for i in range(frameCount-1):
        if debug: print(f'Converting frame {i}')
        grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY) #convert the image to grayscale
        outBuffer.put(grayscaleFrame) #put grayscale frame in buffer
        if debug: print("inserted")
        inputFrame = inBuffer.get() # consume next frame
    print('frame conversion complete')

def displayFrames(inputBuffer):
    # go through each frame in the buffer until the buffer is empty
    global frameCount
    for i in range(frameCount-1):
        # get the next frame
        frame = inputBuffer.get()
        if debug: print(f'Displaying frame {i}')        
        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow('Video', frame)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break
    print('Finished displaying all frames')
    # cleanup the windows
    cv2.destroyAllWindows()

#Get File Name, capture video
fileName = sys.argv[1]
vidcap = cv2.VideoCapture(fileName)
frameCount = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

#shared queues 
inToGS = myQueue(72)
gsToOut = myQueue(72)

#Initialize Threads
extractor = Thread(None, extractFrames, "extractor", [vidcap, inToGS]) #extracts frames from a given file and puts them into a given buffer
converter = Thread(None, convertToGrayScale, "converter", [inToGS, gsToOut]) #extracts frames from a given file and puts them into a given buffer
displayer = Thread(None, displayFrames, "displayer", [gsToOut]) #displays frames from a given buffer

#Start Threads
extractor.start()
converter.start()
displayer.start()