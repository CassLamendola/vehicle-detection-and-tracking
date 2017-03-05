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
[image4]: ./output_images/sliding_windows.png "Windows1"
[image5]: ./output_images/sliding_windows2.png "Windows1.5"
[image6]: ./output_images/sliding_windows3.png "Windows1.75"
[image7]: ./output_images/heat_map_detection.png "Heat"
[image8]: ./output_images/pipleine.png "Pipeline"
________________________________

## Here I will consider the [rubric](https://review.udacity.com/#!/rubrics/513/view) points individually and describe how I addressed each point in my implementation.
________________________________
### Writeup
#### 1. Provide a Writeup that includes all the rubric points and how each one is addressed.

This is it!

### Histogram of Oriented Gradients (HOG)
#### 1. Explain how (and identify where in your code) you extracted HOG features from the training images.

I created a [function]() called `get_hog_features()` which in an image, `orient`, `pix_per_cell`, and `cells_per_block` as inputs. Two other arguments, `vis` for visualization and `feature_vec` for feature vectors, are by default set to `False` and `True` respectively. If `vis` is set to `True`, the function outputs the features along with an image, otherwise it just returns the features.

I then explored different color spaces and different `skimage.hog()` parameters (`orientations`, `pixels_per_cell`, and `cells_per_block`).  I grabbed a random images the training set and displayed it to get a feel for what the `skimage.hog()` output looks like.

Here is an example using the `YUV` color space and HOG parameters of `orientations=8`, `pixels_per_cell=(8, 8)` and `cells_per_block=(2, 2)`:

![alt text][image1]

#### 2. Explain how you settled on your final choice of HOG parameters.

I tried various combinations of parameters and colorspaces and ended up with the same parameters I started with (`orientations=8`, `pixels_per_cell=(8, 8)`, `cells_per_block=(2, 2)` and YUV colorspace.) I decided on those parameters because with them I achieved the best accuracy on some samples from the training set when I implemented an SVM.

####3. Describe how (and identify where in your code) you trained a classifier using your selected HOG features (and color features if you used them).

I first [normalized color features and HOG features]() to prepare for classification. Here is an example of color features before and after normalization:

![alt text][image2]

And here is an example of those color features along with HOG features before and after normalization:

![alt text][image3]

Once the features were normalized, I [trained a linear SVM]() using `LinearSVC()` from sklearn. Though it was the classifier I started with, it achieved 99% accuracy, so I thought it would be unnecessary to try an alternatives.

### Sliding Window Search

#### 1. Describe how (and identify where in your code) you implemented a sliding window search. How did you decide what scales to search and how much to overlap windows?

I created a [function]() called `find_cars()` to search the image for cars. 

Before searching the image with sliding windows, I selected the region of the image where cars would be expected and I converted that entire region to YUV colorspace and got all HOG features for the whole region. Then, with sliding windows, I extracted the HOG features and color features within a given window and used my SVM to predict whether or not the window contained a car. This was more efficient than converting the image and getting HOG features for every individual window.

I then began choosing different scales for window sizes to see which sizes would be appropriate for finding cars. I tried scales of 1, 1.5 and 1.75. Here are examples of what was found for each scale respectively:

![alt text][image4]

![alt text][image5]

![alt text][image6]

On my [final pipeline](), I used 

#### 2. Show some examples of test images to demonstrate how your pipeline is working. What did you do to optimize the performance of your classifier?

Ultimately I searched on the following scales: [1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 3] using YUV 3-channel HOG features plus spatially binned color and histograms of color in the feature vector, which provided a nice result. 

Then I used a heatmap to minimize false positives and eliminate multiple detections of the same car. Here are some example images of the output from my pipeline:

![alt text][image8]

There are some obvious false positives, but these are addressed with the `Vehicles` [class]() which you can read about in the next section.

---

### Video Implementation

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (somewhat wobbly or unstable bounding boxes are ok as long as you are identifying the vehicles most of the time with minimal false positives.)
Here's a [link to my video result]()

#### 2. Describe how (and identify where in your code) you implemented some kind of filter for false positives and some method for combining overlapping bounding boxes.

As mentioned before, I used a [function]() to used a heatmap to reduce false positives. I recorded the positions of positive detections in each frame of the video. From the positive detections I created a heatmap and then thresholded that map to identify vehicle positions. I then used `scipy.ndimage.measurements.label()` to identify individual blobs in the heatmap. I assumed each blob corresponded to a vehicle, and I constructed bounding boxes to covert the area of each blob detected. 

Here's an example result showing the heatmap from a test image and the resulting bounding boxes drawn:

![alt text][image7]

___
### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project. Where will your pipeline likely fail? What could you do to make it more robust?

One problem with my implementation is that it still has problems with detecting false positives. False positives are most commonly detected in the guardrail on an overpass. I could reduce this by collecting more data of those regions from the video, then adding them to my noncar data and retraining.

Also, In a few frames of the output video, one car is "lost". This could be solved by decreasing the threshold for the heatmap. However, if the threshold is decreased without addressing the false positive issue, more false positives will be detected. What I have in my current output is a functional balance between minimal false positives and maximum vehile detection.




