# Vehicle Detection and Tracking
________________________________
## Goals of the project
* Perform a Histogram of Oriented Gradients (HOG) feature extraction on a labeled training set of images
* Apply a color transform and append binned color features, as well as histograms of color, to HOG feature vector
* Normalize features and randomize a selection for training and testing
* Train a classifier (Linear SVM)
* Implement a sliding-window technique and use trained classifier to search for vehicles in images
* Create a heat map of recurring detections frame by frame to reject outliers and follow detected vehicles 
* Estimate a bounding box for vehicles detected
* Draw boxes around detected vehicles

[//]: # (Image References)

[image1]: ./output_images/HOG.png "HOG"
[image2]: ./output_images/normalized_color.png "Normal1"
[image3]: ./output_images/normalized_color_and_hog.png "Normal2"
[image4]: ./output_images/heat_map_detection.png "Heat"
________________________________

## Here I will consider the [rubric](https://review.udacity.com/#!/rubrics/513/view) points individually and describe how I addressed each point in my implementation.
________________________________
### Writeup
#### 1. Provide a Writeup that includes all the rubric points and how each one is addressed.

This is it!

### Histogram of Oriented Gradients (HOG)
#### 1. Explain how (and identify where in your code) you extracted HOG features from the training images.

I created a [function]() called `get_hog_features()` which in an image, `orient`, `pix_per_cell`, and `cells_per_block` as inputs. Two other arguments, `vis` for visualization and `feature_vec` for feature vectors, are by default set to `False` and `True` respectively. If `vis` is set to `True`, the function outputs the features along with an image, otherwise it just returns the features.

Here is an example of a HOG image from the training set:
![alt text][image1]



