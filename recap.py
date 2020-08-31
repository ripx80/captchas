#!/usr/bin/python

#import os, argparse
from PIL import Image,ImageEnhance,ImageFilter,ImageOps
#from pytesseract import image_to_string

import numpy as np
from scipy import ndimage


from features import *
#import cv
import cv2
from matplotlib import pyplot as plt


import os

from utils import *
from filters import *
from models import *


from scipy import misc


class Captcha(object):

    def __init__(self,img_path,tmp_path='tmp',make_copies=True):

        self.il={}
        self.resize_lvl=5
        self.copy_cnt=1

        self.img_path=img_path
        self.tmp_path=tmp_path
        self.make_copies=make_copies
        self.open_image()

        #get infos
        self.x,self.y = self.img.size
        self.mfcolor=self.most_frequent_colour()


        #create the tmp dir
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)

    def info(self):
        print('Size: %dx%d'%(self.x,self.y))
        print('Dominant Color Count: %d, %d'%(self.mfcolor))

    def detect(self):
        pass

    def open_image(self):
        try:
            img=Image.open(self.img_path)
        except:
            print("ERROR: File %s doesn't exist.\n" % self.img_path)
            exit(1)
        #work on copy and convert to L
        #L = R * 299/1000 + G * 587/1000 + B * 114/1000
        self.img=img.convert('L')
        self.make_copy('orig')

    def make_copy(self,title=None):
        if self.make_copies:
            if not title:
                title=self.copy_cnt
            self.il[title]=self.img
            self.copy_cnt+=1

    def print_npix(self):
        print(np.asarray(self.img).transpose())

    def resize_gt(self):
        self.x=int(self.x*self.resize_lvl)
        self.y=int(self.y*self.resize_lvl)
        self.img = self.img.resize((self.x, self.y), Image.BICUBIC)


    def show_il(self):
        for key,value in self.il.items():
            plt.subplot(3,3,self.copy_cnt),plt.imshow(value,'gray')
            plt.title(key)
            plt.xticks([]),plt.yticks([])
            self.copy_cnt+=1
        plt.show()

    def most_frequent_colour(self):
        pixels = self.img.getcolors(self.x * self.y)
        self.mfcolor = pixels[0]
        for count, colour in pixels:
            if count > self.mfcolor[0]:
                self.mfcolor = (count, colour)
        return self.mfcolor



    #Filters -> seperate in extra Class

    def reduce_noise(self):
        #only on Gray Images. Set Pixel to White or Black
        new_img = self.img.copy()
        pix = self.img.load()
        pix2 = new_img.load()
        for x in range(self.x):
            for y in range(self.y):
                color = pix[x,y]
                if color < 127:
                    pix2[x,y] = 0
                else:
                    pix2[x,y] = 255
        self.img=new_img
        #self.make_copy('reduce_noise')


    def load_buff(self):
        self.npix=np.asarray(self.img)

    def blur(self,b):
        self.load_buff()
        return ndimage.gaussian_filter(self.npix, sigma=b)


    def remove_threshold(self,t=4):
        #x=self.blur(5)
        self.load_buff()
        x=ndimage.binary_erosion(self.npix,structure=np.ones((2,2))).astype(self.npix.dtype)
        for i in range(t):
            x=ndimage.binary_erosion(x,structure=np.ones((2,2))).astype(x.dtype)

        #x=ndimage.binary_erosion(self.npix,structure=np.ones((8,8))).astype(self.npix.dtype)
        #self.img=ndimage.binary_erosion(self.img, structure=np.ones((1,1))).astype(self.img.dtype)
        self.img=x
        self.make_copy('Thres')


    def reduce_lines(self,t=1):
        self.load_buff()
        self.img=ndimage.binary_erosion(self.npix,structure=np.ones((t,t))).astype(self.npix.dtype)
        self.make_copy('reduce')

    def thicken_lines(self,t=5):
        self.load_buff()
        x=ndimage.binary_dilation(self.npix).astype(self.npix.dtype)
        for i in range(t):
            x=ndimage.binary_dilation(x).astype(x.dtype)
        self.img=x
        self.make_copy('thicken')


    #call filters

    def clear(self):
        #call following std filters
            #reduce_noise set absolute colors (black or white)
        self.reduce_noise()








#Paths
tmp_path='tmp/out.jpg'
il = {}


img=Captcha('capts/captcha.jpg')
img.info()
img.resize_gt()
img.clear()
img.blur(8)
img.clear()


img.remove_threshold(8)

#img.thicken_lines()
img.remove_threshold(4)
img.reduce_lines()


img.show_il()




exit(1)

### Image Detection###




###Convert to black and white and Filter/Prepare Image


#img = img.convert('L')
#x, y = img.size

#Resize the Image for better detection
#img = img.resize((int(x*5), int(y*5)), Image.BICUBIC)


#img.save(tmp_path,'JPEG')
#il['orig']=img

#work on copy
#img = Image.open(tmp_path)

#Crop the Image
img = crop_img(img)
il['crop']=img

#img.save('./work/crop.jpg')
#Clear the Image
img=reduce_noise(img)
img=smooth(img)
img=reduce_noise(img)
il['reduce_noise']=img

#img.save('./work/reduce_noise.jpg')

#get the dominat color
bgcolor=most_frequent_colour(img)





###Filter#####
img=reduce_lines(img,bgcolor)
img.save('./work/reduce_lines.jpg')

show_il(il)
exit(1)

#Seperate Image

separator=DigitSeparator(img,bgcolor)
for i,d in enumerate(separator.get_digits()):
    print i
    d.image.save('./tmp/diget%d.jpg'%(i))



###func if only one or four pixels. remove

#~ ALL_EXTRACTORS = [
        #~ x_histogram,
        #~ y_histogram,
        #~ positions,
        #~ number_of_whites,
        #~ number_of_pixels,
        #~ horizontal_silhouette,
        #~ reversed_horizontal_silhouette,
        #~ vertical_silhouette,
        #~ reversed_vertical_silhouette,
        #~ middle_silhouette,
        #~ vertical_symmetry,
        #~ horizontal_symmetry,
#~ ]


#Identify Letter
#~ for i,img in enumerate(imgs):
        #~
            #~ #img = intel_crop(img)
            #~ img = img.convert('RGB')
            #~ points,middle = getCenterLine(img,use='center')
            #~ img = img.convert('L')
            #~ img = normalize_sin(img,points,middle)
            #~
            #~ #img = img.convert('L')
            #~
            #~ img = intel_crop(img)
#~
            #~ img = find_angles(img)
#~
            #~ img = img.convert('RGB')
            #~ img = find_breaks(img)
            #~
            #~ img.save(patho+imp+'.'+str(i),'JPEG')
