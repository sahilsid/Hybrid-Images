"""
% Before trying to construct hybrid images, it is suggested that you
% implement my_imfilter.m and then debug it using proj1_test_filtering.m

% Debugging tip: You can split your MATLAB code into cells using "%%"
% comments. The cell containing the cursor has a light yellow background,
% and you can press Ctrl+Enter to run just the code in that cell. This is
% useful when projects get more complex and slow to rerun from scratch
"""

import matplotlib.pyplot as plt
import os
import cv2
from os.path import join
import numpy as np
from PIL import Image
import matplotlib.image as mpimg
from skimage.transform import rescale, resize, downscale_local_mean
from my_imfilter import my_imfilter
from vis_hybrid_image import vis_hybrid_image
import matplotlib.gridspec as gridspec

#%% close all figures
plt.close('all') # closes all figures

#%% Setup
#% read images and convert to floating point format
hybridize=[]

dog = mpimg.imread('../data/dog.bmp').astype('float32')/255
cat = mpimg.imread('../data/cat.bmp').astype('float32')/255
hybridize.append((dog,cat,7))
hybridize.append((cat,dog,12))


bird = mpimg.imread('../data/bird.bmp').astype('float32')/255
plane = mpimg.imread('../data/plane.bmp').astype('float32')/255
hybridize.append((bird,plane,4))
hybridize.append((plane,bird,6))

fish = mpimg.imread('../data/fish.bmp').astype('float32')/255
submarine = mpimg.imread('../data/submarine.bmp').astype('float32')/255
hybridize.append((fish,submarine,5))
hybridize.append((submarine,fish,3))

bicycle = mpimg.imread('../data/bicycle.bmp').astype('float32')/255
motorcycle = mpimg.imread('../data/motorcycle.bmp').astype('float32')/255
hybridize.append((bicycle,motorcycle,7))
hybridize.append((motorcycle,bicycle,6))

einstein = mpimg.imread('../data/einstein.bmp').astype('float32')/255
marilyn = mpimg.imread('../data/marilyn.bmp').astype('float32')/255
hybridize.append((marilyn,einstein,4))
hybridize.append((einstein,marilyn,3))

"""
% Several additional test cases are provided for you, but feel free to make
% your own (you'll need to align the images in a photo editor such as
% Photoshop). The hybrid images will differ depending on which image you
% assign as image1 (which will provide the low frequencies) and which image
% you asign as image2 (which will provide the high frequencies)
"""

""" %% Filtering and Hybrid Image construction """
cutoff_frequency = 5  

"""This is the standard deviation, in pixels, of the 
% Gaussian blur that will remove the high frequencies from one image and 
% remove the low frequencies from another image (by subtracting a blurred
% version from the original version). You will want to tune this for every
% image pair to get the best results. """


def generate_gaussian_filter(shape =(5,5), sigma=1):
    x, y = [  int(edge /2) for edge in shape]
    grid = np.array([[((i**2+j**2)/(2.0*sigma**2)) for i in range(-x, x+1)] for j in range(-y, y+1)])
    g_filter = np.exp(-grid)/(2*np.pi*sigma**2)
    g_filter /= np.sum(g_filter)
    return g_filter

i=0

freq=[3,4,5,6,7,8,9,10,11]

def test_optimum_frequencies():
    for image1,image2 in hybridize:
        i=i+1
        for cutoff_freq in freq:
            fig = plt.figure(cutoff_freq)
            filter = generate_gaussian_filter((cutoff_freq*4+1,cutoff_freq*4+1),cutoff_freq)#insert values from fspecial('Gaussian', cutoff_frequency*4+1, cutoff_frequency) here

            """
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            % YOUR CODE BELOW. Use my_imfilter to create 'low_frequencies' and
            % 'high_frequencies' and then combine them to create 'hybrid_image'
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            % Remove the high frequencies from image1 by blurring it. The amount of
            % blur that works best will vary with different image pairs
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
            """

            low_frequencies = my_imfilter(image1,filter)

            """
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            % Remove the low frequencies from image2. The easiest way to do this is to
            % subtract a blurred version of image2 from the original version of image2.
            % This will give you an image centered at zero with negative values.
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            """

            high_frequencies = image2 - my_imfilter(image2,filter)

            """
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            % Combine the high frequencies and low frequencies
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            """
            hybrid_image = low_frequencies + high_frequencies
            np.clip(hybrid_image,0,1)
            #%% Visualize and save outputs

            # ax1 = fig.add_subplot(gs[0, 0]) # row 0, col 0
            # ax1.imshow(low_frequencies)

            # ax2 = fig.add_subplot(gs[0, 1]) # row 0, col 1
            # ax2.imshow(np.clip(high_frequencies + 0.5,0,1))
            
            vis = vis_hybrid_image(hybrid_image) #see function script vis_hybrid_image.py
            np.clip(vis,0,1)
            
            
            plt.imshow(vis)
            plt.title(cutoff_freq)
        
    # mpimg.imsave('../Results/low_frequencies.jpg',low_frequencies)
    # mpimg.imsave('../Results/high_frequencies.jpg',np.clip(high_frequencies + 0.5,0,1))
    # mpimg.imsave('../Results/hybrid_image.jpg',hybrid_image)
    mpimg.imsave('../Results/hybrid_image_scales.jpg',np.clip(vis,0,1))
    plt.show()

for image1,image2,cutoff_freq in hybridize:
    i=i+1
    p=0
    gs = gridspec.GridSpec(2, 2)
    fig = plt.figure(i)
    filter = generate_gaussian_filter((cutoff_freq*4+1,cutoff_freq*4+1),cutoff_freq)#insert values from fspecial('Gaussian', cutoff_frequency*4+1, cutoff_frequency) here

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % YOUR CODE BELOW. Use my_imfilter to create 'low_frequencies' and
    % 'high_frequencies' and then combine them to create 'hybrid_image'
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Remove the high frequencies from image1 by blurring it. The amount of
    % blur that works best will vary with different image pairs
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
    """

    low_frequencies = my_imfilter(image1,filter)

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Remove the low frequencies from image2. The easiest way to do this is to
    % subtract a blurred version of image2 from the original version of image2.
    % This will give you an image centered at zero with negative values.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    high_frequencies = image2 - my_imfilter(image2,filter)

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Combine the high frequencies and low frequencies
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    hybrid_image = low_frequencies + high_frequencies
    np.clip(hybrid_image,0,1)
    #%% Visualize and save outputs

    ax1 = fig.add_subplot(gs[0, 0]) # row 0, col 0
    ax1.imshow(low_frequencies)
    ax1.set_title('Low Frequency')

    ax2 = fig.add_subplot(gs[0, 1]) # row 0, col 1
    ax2.imshow(np.clip(high_frequencies + 0.5,0,1))
    ax2.set_title('High Frequency')

    vis = vis_hybrid_image(hybrid_image) #see function script vis_hybrid_image.py
    np.clip(vis,0,1)
    ax3 = fig.add_subplot(gs[1, :])
    ax3.imshow(vis)
    ax3.set_title('Hybrid Image')
    plt.title(i)

    mpimg.imsave('../Results/low_frequencies_'+str(i)+'.jpg',np.clip(low_frequencies,0,1))
    mpimg.imsave('../Results/high_frequencies_'+str(i)+'.jpg',np.clip(high_frequencies + 0.5,0,1))
    mpimg.imsave('../Results/hybrid_image_'+str(i)+'.jpg',np.clip(hybrid_image,0,1))
    mpimg.imsave('../Results/hybrid_image_scales_'+str(i)+'.jpg',np.clip(vis,0,1))
    plt.savefig('../Results/final/'+str(i)+'.png')
plt.show()