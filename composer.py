import numpy as np
import cv2
import matplotlib.pyplot as plt
import video

class composer:
    def __init__(self) :
        self.matrix=None
        self.mask_inverse= None
        self.temp_count=0

    def temp_combine(self,video_frame,trailer_frame):
        if(self.matrix is None or self.temp_count>3):
            return video_frame

        overlay = cv2.warpPerspective(trailer_frame,self.matrix,(video_frame.shape[1],video_frame.shape[0]))   
        masked_frame = cv2.bitwise_and(video_frame,video_frame,mask=self.mask_inverse)
        output_frame = cv2.bitwise_or(overlay,masked_frame)
        self.temp_count+=1
        return output_frame
        


    def combine(self,book,video_frame,trailer_frame):
        
        #  Get cover size
        tH,tW,tC=book.cover.shape

        # Adjust trailer size
        trailer_frame = cv2.rotate(trailer_frame, cv2.cv2.ROTATE_90_CLOCKWISE)
        trailer_frame = cv2.resize(trailer_frame,(tW,tH))

        # Creat sift obj
        sift = cv2.SIFT_create()

        # Get book cover key points
        if(book.kp==None):
            kp1, des1 = sift.detectAndCompute(book.cover,None)
            book.kp=kp1
            book.des=des1
        else:
            kp1 = book.kp
            des1=book.des
        # Get frame key points   
        kp2, des2 = sift.detectAndCompute(video_frame,None)

        # Match features and set the best in good
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1,des2,k=2)
        good = []
        for m,n in matches:
            if m.distance < 0.75* n.distance:
                good.append(m)

        # If there are not enough good points use previous data
        if(len(good)<100):
            return self.temp_combine(video_frame,trailer_frame)

        self.temp_count=0

        #matched_features = cv2.drawMatches(book.cover,kp1,video_frame,kp2,good,None, flags=2)

        #Get the positions of  best points 
        scr_points = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
        dst_points = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1,1,2)

        # Find transform matrix
        matrix, mask = cv2.findHomography(scr_points,dst_points,cv2.RANSAC,5)
        self.matrix=matrix

        # Convert cover corners point to frame space
        points = np.float32([[0,0],[0,tH],[tW,tH],[tW,0]]).reshape(-1,1,2)
        dest = cv2.perspectiveTransform(points,matrix)

        #img4=cv2.polylines(frame_image,[np.int32(dest)],True,(255,0,255),3)

        # create overlay image of target(trailer_frame)
        cover_overlay = cv2.warpPerspective(trailer_frame,matrix,(video_frame.shape[1],video_frame.shape[0]))

        mask = np.zeros((video_frame.shape[0],video_frame.shape[1]),np.uint8)
        cv2.fillPoly(mask,[np.int32(dest)],(255,255,255))
        self.mask_inverse = cv2.bitwise_not(mask)

        output_frame = video_frame
        # Masked frame
        masked_frame = cv2.bitwise_and(output_frame,output_frame,mask=self.mask_inverse)
        # Add img_overlay to frame
        output_frame = cv2.bitwise_or(cover_overlay,masked_frame)

        return  output_frame