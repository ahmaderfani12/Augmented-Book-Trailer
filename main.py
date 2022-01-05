import numpy as np
import cv2
import VideoEdit as video
from book import book
from find_book import find_best_cover
from composer import composer


#Load book and trailers
books=[]
# books.append(book('Angels and Demons',cv2.imread("files/Angels and Demons.jpg",1),"files/Angels and Demons.mp4"))
# books.append(book('Anne of Green Gables & Anne of Avonlea',cv2.imread("files/Anne of Green Gables & Anne of Avonlea.jpg",1),"files/Anne of Green Gables & Anne of Avonlea.mp4"))
books.append(book('David Copperfield',cv2.imread("files/David Copperfield.jpg",1),"files/David Copperfield.mp4"))
# books.append(book('Dracula',cv2.imread("files/Dracula.jpg",1),"files/Dracula.mp4"))
# books.append(book('Pickwick Papers',cv2.imread("files/Pickwick Papers.jpg",1),"files/Pickwick Papers.mp4"))
# books.append(book('To Kill a Mockingbird',cv2.imread("files/To Kill a Mockingbird.jpg",1),"files/To Kill a Mockingbird.mp4"))
# books.append(book('Tom Sawyer and Huckleberry Finn',cv2.imread("files/Tom Sawyer and Huckleberry Finn.jpg",1),"files/Tom Sawyer and Huckleberry Finn.mp4"))
# books.append(book('Twenty Thousand Leagues Under the Sea',cv2.imread("files/Twenty Thousand Leagues Under the Sea.jpg",1),"files/Twenty Thousand Leagues Under the Sea.mp4"))
# books.append(book('Twilight - Eclipse',cv2.imread("files/Twilight - Eclipse.jpg",1),"files/Twilight - Eclipse.mp4"))
# books.append(book('Twilight - New Moon',cv2.imread("files/Twilight - New Moon.jpeg",1),"files/Twilight - New Moon.mp4"))



# Input video*
vidcap = cv2.VideoCapture('files/Test/0.MOV')
success,video_frame = vidcap.read()
video_length=int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

count = 0
best_book = None
out_frames=[]
compos = composer()

while success:    
    success,video_frame = vidcap.read()
    if(success):
        # Find the best book based on similar features
        best_book = find_best_cover(books,video_frame,best_book)
        out_frame = video_frame

        # Get trailer
        if(best_book.video==None):
            trailer = cv2.VideoCapture(best_book.video_address)
            best_book.video=trailer
        else:
            trailer=best_book.video

        # Get trailer frame
        trailer.set(cv2.CAP_PROP_POS_FRAMES,best_book.last_frame)
        success,trailer_frame = trailer.read()

        # Process augmented frame
        out_frame = compos.combine(best_book,video_frame,trailer_frame)

        best_book.last_frame+=1
        count += 1

        out_frames.append(out_frame)
        print("Frame: "+str(count)+"/"+str(video_length))


video.save_video(out_frames,'output.mp4')



