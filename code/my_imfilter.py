# -*- coding: utf-8 -*-
"""
% This function that you will implement is intended to behave like the built-in function 
% imfilter() in Matlab or equivalently the same function implemented as part of scipy.misc module
% in Python. You will implement imfilter from first principles, i.e., without using 
% any library functions. 

% See 'help imfilter' or 'help conv2'. While terms like "filtering" and
% "convolution" might be used interchangeably, we will essentially perform 2D correlation 
% between the filter and image. Referring to 'proj1_test_filtering.py' would help you with
% your implementation. 
  
% Your function should work for color images. Simply filter each color
% channel independently.

% Your function should work for filters of any width and height
% combination, as long as the width and height are odd (e.g. 1, 7, 9). This
% restriction makes it unambigious which pixel in the filter is the center
% pixel.

% Boundary handling can be tricky. The filter can't be centered on pixels
% at the image boundary without parts of the filter being out of bounds. If
% you look at 'help conv2' and 'help imfilter' in Matlab, you see that they have
% several options to deal with boundaries. You should simply recreate the
% default behavior of imfilter -- pad the input image with zeros, and
% return a filtered image which matches the input resolution. A better
% approach would be to mirror the image content over the boundaries for padding.

% % Uncomment if you want to simply call library imfilter so you can see the desired
% % behavior. When you write your actual solution, **you can't use imfilter,
% % correlate, convolve commands, but implement the same using matrix manipulations**. 
% % Simply loop over all the pixels and do the actual
% % computation. It might be slow.
"""
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import scipy.ndimage as s
import numpy as np
from skimage import color
from skimage import io
import os
from vis_hybrid_image import vis_hybrid_image

# print(os.path.join(os.path.dirname(os.getcwd())),'data/')
imgInputPath=os.path.join(os.path.dirname(os.getcwd()),'data/')

bird = mpimg.imread(os.path.join(imgInputPath,'bird.bmp'))
plane = mpimg.imread(os.path.join(imgInputPath,'plane.bmp')) 

""" Exemplar Gaussian 3x3 filter shown below-- see filters defined in proj1_test_filtering.py """

def gauss2D(shape=(3,3),sigma=0.5):
    """
    2D gaussian mask - should give the same result as MATLAB's
    fspecial('gaussian',[shape],[sigma])
    """
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h

class my_image_editor(object):
  def __init__(self,image,zero_padding='True'):
    
   
    self.zero_padding=False
    self.rgb = False

    self.filters = {
      'gaussian'  : np.asarray([[0.1019,0.1154,0.1019],[0.1154,0.1308,0.1154],[0.1019,0.1154,0.1019]],dtype=np.float32) ,
      'laplace'   : np.asarray([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]),
      'high_pass' : np.asarray([[0,-0.25,0],[-0.25,2,-0.25],[0,-0.25,0]]),
      'low_pass'  : np.asarray([[0,0.25,0],[0.25,-2,0.25],[0,0.25,0]])
    }

    self.kernel = np.asarray([[0,0,0],[0,1,0],[0,0,0]],dtype=np.float32) 
    

    # elif(len(kernel.shape==2) or len(kernel.shape==3)):
    #   self.kernel=kernel

    self.image=image
    self.channels = int(1)
    
    if(len(image.shape)==3 and image.shape[2]==3):
      self.rgb=True
      self.channels = 3

    if(not self.rgb):
      self.image = self.image[:,:,np.newaxis]
    self.image_height   = self.image.shape[0]
    self.image_width    = self.image.shape[1]
    self.zero_padding   = zero_padding

    
  def set_kernel(self,filter='none'): 
    if(filter=='none'):
      self.kernel = np.asarray([[0,0,0],[0,1,0],[0,0,0]],dtype=np.float32) 
    
    elif(not( (type(filter) is np.ndarray)) and filter in self.filters):
      self.kernel = self.filters[filter]
    
    elif( (type(filter) is np.ndarray) and (len(filter.shape)==2) or len(filter.shape)==3):
      self.kernel=filter

    else:
      print('\nInvalid Filter.\n')
      return False

    if(self.rgb and len(self.kernel.shape)==2):
      self.kernel = np.tile(self.kernel[:,:,None],[1,1,3])
    else:
      self.kernel=self.kernel[:,:,np.newaxis]
    return True

  # Straight Forward Slow Method. Better Method implemented using np.sum(np.multiply())
  # def convolveStep(self,x,y):
  #       filter=self.kernel
  #       sum = 0
  #       height  = self.image.shape[0]
  #       width   = self.image.shape[1]

  #       filter_height   = filter.shape[0]
  #       filter_width    = filter.shape[1]
        
  #       for f_x in range(-1*int(filter_height/2),int(filter_height/2)+1):
  #           x_offset = x+f_x
  #           if(x_offset>=0 and x_offset<height):
  #             for f_y in range(-1*int(filter_width/2),int(filter_width/2)+1):                  
  #                 y_offset = y+f_y
  #                 if(y_offset>=0 and y_offset<width):
  #                         add = np.multiply(self.image[x_offset][y_offset],filter[int(filter_height/2)+f_x][int(filter_width/2)+f_y])
  #                         sum = sum + add
                        
  #                 else:
  #                     if(not self.zero_padding):
  #                         return self.image[x][y]
                        
  #       return sum

  def my_2DConvolution(self):
    filter=self.kernel
    
    f_height   = filter.shape[0]
    f_width    = filter.shape[1]

    #Flipping the Kernel Along Both X and Y Axis so that in convolution straight sum of products with image can be taken
    filter = np.flip(filter)
    
    # print('Image  Shape : ',self.image.shape)
    # print('Filter Shape : ',filter.shape)
    
    if(filter.shape[0]%2==0 or filter.shape[1]%2==0 ):
      print("Error : Filter size is even. \n")
      return  

    row_padding = int((f_height-1)/2)
    col_padding = int((f_width-1)/2)
    
    self.zero_padded_image = np.zeros((self.image_height+row_padding*2,self.image_width+col_padding*2,self.channels))
    self.zero_padded_image[row_padding:self.image_height+row_padding,col_padding:self.image_width+col_padding]=self.image
    
    ##View The Zero Padded Image
    #plt.imshow(self.zero_padded_image/255)
    #plt.show()
    
    output_image = np.zeros(self.image.shape)
    for row_pixel in range(row_padding,self.image_height+row_padding):
        for col_pixel in range (col_padding,self.image_width+col_padding):
            stepValue = np.sum(np.sum(np.multiply(filter,self.zero_padded_image[row_pixel-row_padding:row_pixel+row_padding+1,col_pixel-col_padding:col_pixel+col_padding+1]),axis = 0),axis = 0)
            #convStep = self.convolveStep(row_pixel-row_padding,col_pixel-col_padding)
            output_image[row_pixel-row_padding][col_pixel-col_padding]= stepValue
              

    if(self.rgb==False):
      output_image=np.squeeze(output_image)

    return output_image

  def apply_filter(self,filter='none'):
    if(self.set_kernel(filter)):
      return self.my_2DConvolution()

def my_imfilter(image,filter,zero_padding=False):  #which will work identically to the function below
  editor = my_image_editor(image,zero_padding=zero_padding)
  return np.clip(editor.apply_filter(filter),0,1)

def my_hybrid_image(image1,image2):
  image1 = my_image_editor(image1)
  image2 = my_image_editor(image2)
  cutoff_frequency = 8
  # This is the standard deviation, in pixels, of the 
  # Gaussian blur that will remove the high frequencies from one image and 
  # remove the low frequencies from another image (by subtracting a blurred
  # version from the original version). You will want to tune this for every
  # image pair to get the best results.
  gaussian_filter = gauss2D(shape=(cutoff_frequency*4+1,cutoff_frequency*4+1), sigma = cutoff_frequency)

  lowfreq = image2.apply_filter(gaussian_filter)
  highfreq = image1.image - image1.apply_filter(gaussian_filter)
  return (lowfreq + highfreq)

# def rgb2gray(rgb):
    # return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])
# testData=np.array([[1,2,3],[4,5,6],[7,8,9]])
# testFilter=np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
# output = my_hybrid_image(bird,plane)
# plt.figure(1)
# plt.title("Hybrid")
# plt.imshow(my_imfilter(rgb2gray(bird/255),gauss2D()),cmap='gray')

# # plt.figure(3)
# # plt.title("original")
# # plt.imshow(img)


# plt.show()
