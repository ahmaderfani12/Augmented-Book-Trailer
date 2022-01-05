import numpy as np
import cv2
from book import book

def find_best_cover(books,input_image,last_best=None):

    if(last_best):
        best_feature_number=last_best.features
    else:
        best_feature_number=0

    best_book = last_best

    orb = cv2.ORB_create(1000)
    kp2, des2 = orb.detectAndCompute(input_image,None)
    # Find the most similar book in the frame
    for b in books:
        cover = b.cover
        kp1, des1 = orb.detectAndCompute(cover,None)
        if(kp2==None or kp1 == None):
            continue

        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1,des2,k=2)
        good = []
        for m,n in matches:
            if m.distance < 0.75* n.distance:
                good.append(m)
        if(len(good)>best_feature_number):
            best_feature_number = len(good)
            best_book=b
    # print('good features: '+ str(len(good)))
    best_book.features=len(good)
    return  best_book
