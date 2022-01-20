
import cv2

def save_frames(video_location,save_location):
  vidcap = cv2.VideoCapture(video_location)
  success,image = vidcap.read()
  count = 0
  while success:
    cv2.imwrite(save_location+"/frame%d.jpg" % count, image)     # save frame as JPEG file      
    success,image = vidcap.read()
    # print('Read a new frame: ', success)
    count += 1

def save_video(frames, address):
  height, width, layers = frames[0].shape
  size = (width,height)

  out_video = cv2.VideoWriter(address,0x7634706d , 20.0, size)
  for i in range(len(frames)):
    out_video.write(frames[i])
  out_video.release()
