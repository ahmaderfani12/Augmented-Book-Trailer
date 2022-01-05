# Augmented-Book-Trailer
## About The Project
This was one of my computer vision homework in Fall 2021.
A database contains the cover of some books and  movie trailers based on them. The goal is to get an input video, find a relevant book, and project its movie trailer on the cover.
## Summary of process
1. Get the books database(Here I simply create book objects in the main module)
2. Read input video frames and find the best-matched book using ORB feature matching.
3. Use open cv Homography to estimate a homography that fits all corresponding points.
4. Use the homography matrix to convert the trailer corner's position in video space.
Create a mask using new corner positions.
5. Add trailer frame to input video using the mask.
    <br />
    <br />
![alt text](https://github.com/ahmaderfani12/Augmented-Book-Trailer/blob/master/files/Readme/process.png)
    <br />
    <br />
## Output
As our input is full of detail from other books and sometimes our cover is so simple and doesn't provide enough feature points, there are many frames with misinterpreting with other books. To solve this issue, I keep the last good data ( converted positions) and reuse them when there are not enough features.
    <br />
    <br />
Raw output:
    <br />
![alt text](https://github.com/ahmaderfani12/Augmented-Book-Trailer/blob/master/files/Readme/raw_out.gif?raw=true)
    <br />
Using previous data in misinterpretations:
    <br />
![alt text](https://github.com/ahmaderfani12/Augmented-Book-Trailer/blob/master/files/Readme/stacked_out.gif?raw=true)

## Getting Started
You can easily add you book data in books arrays and change input video address at main module.
