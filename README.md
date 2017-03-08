## Vehicle Detection and Tracking

In this project, the goal was to write a software pipeline to search for vehicles in a video and track them throughout frames. Check out my [writeup](https://github.com/CassLamendola/vehicle-detection-and-tracking/blob/master/writeup.md) for this project for more details.  

The Project
---

The goals / steps of this project are the following:

* Perform a Histogram of Oriented Gradients (HOG) feature extraction on a labeled training set of images
* Apply a color transform and append binned color features, as well as histograms of color, to HOG feature vector
* Normalize features and randomize a selection for training and testing
* Train a classifier (Linear SVM)
* Implement a sliding-window technique and use trained classifier to search for vehicles in images
* Create a heat map of recurring detections frame by frame to reject outliers and follow detected vehicles 
* Estimate a bounding box for vehicles detected
* Draw boxes around detected vehicles

The images in `test_images` were used for testing my pipeline on single frames. I've saved examples of the output from each stage of my pipeline in the folder called `ouput_images`, and included a description in the writeup for the project of what each image shows. I first tested my pipeline on test images, then on the test video called `test_video.mp4`. The video called `project_video.mp4` is the video my pipeline was designed to work on.