import cv
from PIL import Image

def pil2cv(img,t='L'):
    if t == 'L':
        res = cv.CreateImageHeader(img.size, 8, 1)
    else:
        res = cv.CreateImageHeader(img.size, 32, 3)
    cv.SetData(res, img.tostring())
    return res

def cv2pil(img,t='L'):

    img = Image.fromstring(t, cv.GetSize(img), img.tostring())

    return img

def togrey(img):
    image_gray = cv.CreateImage(cv.GetSize(img),8,1)
    cv.CvtColor(img,image_gray,cv.CV_RGB2GRAY)

    return image_gray

def torgb(img):
    image = cv.CreateImage(cv.GetSize(img),32,3)
    cv.CvtColor(img,image,cv.CV_GRAY2RGB)

    return image


def most_frequent_colour(image):
    w, h = image.size
    pixels = image.getcolors(w * h)
    most_frequent_pixel = pixels[0]
    for count, colour in pixels:
        if count > most_frequent_pixel[0]:
            most_frequent_pixel = (count, colour)
    return most_frequent_pixel[1]
    #return most_frequent_pixel

##croping
def crop_img(img,xstop = 0.02,ystop = 0.02):
    y1 = x1 = x2 = y2 = 0
    bufimg = img.load()
    for y in xrange(img.size[1]):
        count = 0
        for x in xrange(img.size[0]):
            if bufimg[x,y] < 120:
                count += 1
        if count*1.0/img.size[0] >= ystop:
            y1 = y
            break
    for y in xrange(img.size[1]-1,0,-1):
        count = 0
        for x in xrange(img.size[0]):
            if bufimg[x,y] < 120:
                count += 1
        if count*1.0/img.size[0] >= ystop:
            y2 = y
            break
    for x in xrange(img.size[0]):
        count = 0
        for y in xrange(img.size[1]):
            if bufimg[x,y] < 120:
                count += 1
        if count*1.0/img.size[1] >= xstop:
            x1 = x
            break
    for x in xrange(img.size[0]-1,0,-1):
        count = 0
        for y in xrange(img.size[1]):
            if bufimg[x,y] < 120:
                count += 1
        if count*1.0/img.size[1] >= xstop:
            x2 = x
            break
    img_trans=img.transform((x2-x1,y2-y1),Image.EXTENT, (x1,y1,x2,y2))
    return img_trans
