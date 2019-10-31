import matplotlib.pyplot as plt
import os
import cv2
from os.path import join
import numpy as np
from PIL import Image
import matplotlib.image as mpimg
from skimage.transform import rescale, resize, downscale_local_mean


hybridize=[]

dog = mpimg.imread('../data/dog.bmp').astype('float32')/255
cat = mpimg.imread('../data/cat.bmp').astype('float32')/255
hybridize.append((dog,cat))

bird = mpimg.imread('../data/bird.bmp')
plane = mpimg.imread('../data/plane.bmp')
hybridize.append((bird,plane))

fish = mpimg.imread('../data/fish.bmp')
submarine = mpimg.imread('../data/submarine.bmp')
hybridize.append((fish,submarine))

bicycle = mpimg.imread('../data/bicycle.bmp')
motorcycle = mpimg.imread('../data/motorcycle.bmp')
hybridize.append((bicycle,motorcycle))

einstein = mpimg.imread('../data/einstein.bmp')
marilyn = mpimg.imread('../data/marilyn.bmp')
hybridize.append((einstein,marilyn))

for image1,image2 in hybridize:
    print(image1,image2.dtype)
    break