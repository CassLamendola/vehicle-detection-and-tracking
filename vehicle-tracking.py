import numpy as np
import cv2
from skimage.feature import hog
import matplotlib.image as mpimg
import glob
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC
import time
from sklearn.model_selection import train_test_split

# Global variables
ORIENT = 8
PIX_PER_CELL = 8
CELL_PER_BLOCK = 2

# Here is a helper function for visualizing and saving output
def plot_imgs(imgs, titles, figsize=(24, 9), cmap='gray', save=False):
    # Number of images
    num_imgs = len(imgs)
    
    # Plot just one image
    if num_imgs == 1:
        f, ax = plt.subplots(nrows=1, ncols=1)
        ax.imshow(imgs)
        ax.set_title(titles)
    
    # Create figure
    else:
        f, axes = plt.subplots(1, num_imgs, figsize=figsize)
        f.tight_layout()
        for i in range(num_imgs):
            axes[i].imshow(imgs[i], cmap=cmap)
            axes[i].set_title(titles[i], fontsize=50)
        
    # Save figure
    if save == True:
        plt.savefig('./output_images/' + titles[-1] + '.png', bbox_inches='tight')
    plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)

# Get HOG features from an image
def get_hog_features(img, orient, pix_per_cell, cell_per_block, 
                        vis=False, feature_vec=True):
    # Call with two outputs if visualizing output
    if vis == True:
        features, hog_image = hog(img, orientations=orient, 
                                  pixels_per_cell=(pix_per_cell, pix_per_cell),
                                  cells_per_block=(cell_per_block, cell_per_block), 
                                  transform_sqrt=False, 
                                  visualise=vis, feature_vector=feature_vec)
        return features, hog_image
    # Otherwise call with one output
    else:      
        features = hog(img, orientations=orient, 
                       pixels_per_cell=(pix_per_cell, pix_per_cell),
                       cells_per_block=(cell_per_block, cell_per_block), 
                       transform_sqrt=False, 
                       visualise=vis, feature_vector=feature_vec)
        return features

# Convert to specified colorspace
def convert_color(img, conv='RGB2YUV'):
    if conv == 'RGB2YUV':
        return cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    elif conv == 'RGB2YCrCb':
        return cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
    elif conv == 'RGB2HLS':
        return cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    elif conv == 'RGB2LUV':
        return cv2.cvtColor(img, cv2.COLOR_RGB2LUV)
    elif conv == 'RGB2HSV':
        return cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

# Bin color features    
def bin_spatial(img, size=(32, 32)):
    color1 = cv2.resize(img[:,:,0], size).ravel()
    color2 = cv2.resize(img[:,:,1], size).ravel()
    color3 = cv2.resize(img[:,:,2], size).ravel()
    return np.hstack((color1, color2, color3))

# Histogram of colors
def color_hist(img, nbins=32, bins_range=(0, 256)):
    # Compute the histogram of the color channels separately
    channel1_hist = np.histogram(img[:,:,0], bins=nbins)
    channel2_hist = np.histogram(img[:,:,1], bins=nbins)
    channel3_hist = np.histogram(img[:,:,2], bins=nbins)
    
    # Concatenate the histograms into a single feature vector
    hist_features = np.concatenate((channel1_hist[0], channel2_hist[0], channel3_hist[0]))
    
    # Return the individual histograms, bin_centers and feature vector
    return hist_features

# Extract features from a list of images
def get_color_features(imgs, conv='RGB2YUV', spatial_size=(32, 32),
                        hist_bins=32, hist_range=(0, 256)):
    # Create a list to append feature vectors to
    features = []
    # Iterate through the list of images
    for img in imgs:
        # Read in each one by one
        img = mpimg.imread(img)
        # apply color conversion
        img = convert_color(img, conv='RGB2YUV')
        # Apply bin_spatial() to get spatial color features
        color_features = bin_spatial(img, size=spatial_size)
        # Apply color_hist() to get color histogram features
        hist_features = color_hist(img, nbins=hist_bins, bins_range=hist_range)
        # Append the new feature vector to the features list
        features.append(np.concatenate((color_features, hist_features)))
    # Return list of feature vectors
    return features

# Combine HOG features with color features
def extract_features(imgs, conv='RGB2YUV', orient=ORIENT, hog_channel=0,
                        pix_per_cell=PIX_PER_CELL, cell_per_block=CELL_PER_BLOCK,
                        spatial_size=(32, 32), hist_bins=32, hist_range=(0, 256)):
    # Create a list to append feature vectors to
    features = []
    # Iterate through the list of images
    for file in imgs:
        # Read in each one by one
        img = mpimg.imread(file)
        # apply color conversion
        img = convert_color(img, conv='RGB2YUV')      
        # Apply bin_spatial() to get spatial color features
        color_features = bin_spatial(img, size=spatial_size)
        # Apply color_hist() to get color histogram features
        hist_features = color_hist(img, nbins=hist_bins, bins_range=hist_range)
        # Call get_hog_features() with vis=False, feature_vec=True
        if hog_channel == 'ALL':
            hog_features = []
            for channel in range(img.shape[2]):
                hog_features.append(get_hog_features(img[:,:,channel], 
                                    orient, pix_per_cell, cell_per_block, 
                                    vis=False, feature_vec=True))
            hog_features = np.ravel(hog_features)        
        else:
            hog_features = get_hog_features(img[:,:,hog_channel], orient, 
                        pix_per_cell, cell_per_block, vis=False, feature_vec=True)
        # Append the new feature vector to the features list
        features.append(np.concatenate((color_features, hist_features, hog_features)))
    # Return list of feature vectors
    return features

car_features = extract_features(cars, conv='RGB2YUV', hog_channel='ALL', spatial_size=(32, 32),
                        hist_bins=32, hist_range=(0, 256))
notcar_features = extract_features(notcars, conv='RGB2YUV', hog_channel='ALL', spatial_size=(32, 32),
                        hist_bins=32, hist_range=(0, 256))

# Normalize features
if len(car_features) > 0:
    # Create an array stack of feature vectors
    X = np.vstack((car_features, notcar_features)).astype(np.float64)                        
    # Fit a per-column scaler
    X_scaler = StandardScaler().fit(X)
    # Apply the scaler to X
    scaled_X = X_scaler.transform(X)
    car_ind = np.random.randint(0, len(cars))

# Train a classifier on the normalized features
y = np.hstack((np.ones(len(car_features)), np.zeros(len(notcar_features))))

# Split up data into randomized training and test sets
rand_state = np.random.randint(0, 100)
X_train, X_test, y_train, y_test = train_test_split(
    scaled_X, y, test_size=0.2, random_state=rand_state)

# Use a linear SVC 
svc = LinearSVC()
svc.fit(X_train, y_train)

# Check the score of the SVC
print('Test Accuracy of SVC = ', round(svc.score(X_test, y_test), 4))

# Check the prediction time for a single sample
t=time.time()
svc.predict(X_test)
t2 = time.time()
print(round(t2-t, 5), 'Seconds to predict')

# Extract features using hog sub-sampling and make predictions
def find_cars(img, ystart, ystop, scale, svc, orient, pix_per_cell, cell_per_block, spatial_size, hist_bins):
    
    draw_img = np.copy(img)
    img = img.astype(np.float32)/255
    box_list = []
    
    img_tosearch = img[ystart:ystop,:,:]
    ctrans_tosearch = convert_color(img_tosearch, conv='RGB2YUV')
    if scale != 1:
        imshape = ctrans_tosearch.shape
        ctrans_tosearch = cv2.resize(ctrans_tosearch, (np.int(imshape[1]/scale), np.int(imshape[0]/scale)))
        
    ch1 = ctrans_tosearch[:,:,0]
    ch2 = ctrans_tosearch[:,:,1]
    ch3 = ctrans_tosearch[:,:,2]

    # Define blocks and steps as above
    nxblocks = (ch1.shape[1] // pix_per_cell)-1
    nyblocks = (ch1.shape[0] // pix_per_cell)-1 
    nfeat_per_block = orient*cell_per_block**2
    
    # 64 was the orginal sampling rate, with 8 cells and 8 pix per cell
    window = (pix_per_cell * pix_per_cell)
    nblocks_per_window = (window // pix_per_cell)-1 
    cells_per_step = 2  # Instead of overlap, define how many cells to step
    nxsteps = (nxblocks - nblocks_per_window) // cells_per_step
    nysteps = (nyblocks - nblocks_per_window) // cells_per_step
    
    # Compute individual channel HOG features for the entire image
    hog1 = get_hog_features(ch1, orient, pix_per_cell, cell_per_block, feature_vec=False)
    hog2 = get_hog_features(ch2, orient, pix_per_cell, cell_per_block, feature_vec=False)
    hog3 = get_hog_features(ch3, orient, pix_per_cell, cell_per_block, feature_vec=False)
    
    for yb in range(nysteps):
        for xb in range(nxsteps):
            ypos = yb*cells_per_step
            xpos = xb*cells_per_step
            
            # Extract HOG for this patch
            hog_feat1 = hog1[ypos:ypos+nblocks_per_window, xpos:xpos+nblocks_per_window].ravel() 
            hog_feat2 = hog2[ypos:ypos+nblocks_per_window, xpos:xpos+nblocks_per_window].ravel() 
            hog_feat3 = hog3[ypos:ypos+nblocks_per_window, xpos:xpos+nblocks_per_window].ravel() 
            hog_features = np.hstack((hog_feat1, hog_feat2, hog_feat3))

            xleft = xpos*pix_per_cell
            ytop = ypos*pix_per_cell

            # Extract the image patch
            subimg = cv2.resize(ctrans_tosearch[ytop:ytop+window, xleft:xleft+window], (32,32))
          
            # Get color features
            spatial_features = bin_spatial(subimg, size=spatial_size)
            hist_features = color_hist(subimg, nbins=hist_bins)

            # Scale features and make a prediction
            test_features = X_scaler.transform(np.hstack((spatial_features, hist_features, hog_features)).reshape(1, -1))    
            test_prediction = svc.predict(test_features)
            
            if test_prediction == 1:
                xbox_left = np.int(xleft*scale)
                ytop_draw = np.int(ytop*scale)
                win_draw = np.int(window*scale)
                box_list.append(((xbox_left, ytop_draw+ystart), (xbox_left+win_draw,ytop_draw+win_draw+ystart)))
                cv2.rectangle(draw_img,(xbox_left, ytop_draw+ystart),(xbox_left+win_draw,ytop_draw+win_draw+ystart),(0,0,255),6) 
                
    return draw_img, box_list

# Create a heat map of recurring detections frame by frame to reject outliers and follow detected vehicles
from scipy.ndimage.measurements import label

def add_heat(heatmap, bbox_list):
    # Iterate through list of bboxes
    for box in bbox_list:
        # Add 1 for all pixels inside each bounding box
        heatmap[box[0][1]:box[1][1], box[0][0]:box[1][0]] += 1

    # Return updated heatmap
    return heatmap

def apply_threshold(heatmap, threshold):
    # Zero out pixels below the threshold
    heatmap[heatmap <= threshold] = 0
    
    # Return thresholded map
    return heatmap

def draw_labeled_bboxes(img, labels):
    # Iterate through all detected cars
    for car_number in range(1, labels[1]+1):
        # Find pixels with each car_number label value
        nonzero = (labels[0] == car_number).nonzero()
        
        # Identify x and y values of those pixels
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])
        
        # Define a bounding box based on min/max x and y
        bbox = ((np.min(nonzerox), np.min(nonzeroy)), (np.max(nonzerox), np.max(nonzeroy)))
        
        # Draw the box on the image
        cv2.rectangle(img, bbox[0], bbox[1], (0,0,255), 6)
    # Return the image
    return img

# Create a class to keep track of recentely detected cars
class Vehicles:
    def __init__(self):
        self.bboxes = []
        self.frames = 0
        self.max_frames = 5
    
    def bbox_new(self, bboxes):
        self.bboxes.append(bboxes)
        if self.frames >= self.max_frames:
            self.bboxes = self.bboxes[8:]
            self.frames -= 1
            
    def heatmap(self, img):
        heat = np.zeros_like(img[:,:,0]).astype(np.float)
        for bboxes in self.bboxes:
            # Add heat to each box in box list
            heat = add_heat(heat, bboxes)
        # Apply threshold to help remove false positives
        heat = apply_threshold(heat, 5)
        return heat

# Create a pipeline to detect cars in video
def pipeline(img, threshold=35):
    # Search for cars with sliding windows
    scales = [1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 3]
    
    # Search for cars using windows of each scale
    for scale in (scales):
        out_img, box_list = find_cars(img, ystart, ystop, scale, svc, ORIENT, PIX_PER_CELL, CELL_PER_BLOCK, (32, 32), 32)
        detected_vehicles.bbox_new(box_list)
        
    detected_vehicles.frames +=1
    
    # Find final boxes from heatmap using label function
    heat = detected_vehicles.heatmap(img, threshold)
    heatmap = np.clip(heat, 0, 255)
    labels = label(heatmap)
    img = draw_labeled_bboxes(img, labels)
    return img