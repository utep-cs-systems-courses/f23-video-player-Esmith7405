import ExtractAndDisplay as video
import queue

#Execute each segment concurrently

# filename of clip to load
filename = 'clip.mp4'
# shared queue  
buff = queue.Queue()

#Extract Frames
video.extractFrames(filename,buff, 72)

#Convert Frames

#Display Frames
video.displayFrames(buff)
