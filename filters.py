##filters
from PIL import Image,ImageEnhance,ImageFilter,ImageOps
def _get(pix, (width,height), coord, default=0):
    x, y = coord
    if (x>=width) or (x<0) or (y>=height) or (y<0):
        return default
    else:
        return pix[x,y]

def reduce_noise(image):
    #only on Gray Images. Set Pixel to White or Black
    new_img = image.copy()
    width, height = image.size
    pix = image.load()
    pix2 = new_img.load()
    for x in range(width):
        for y in range(height):
            color = pix[x,y]
            if color < 127:
                pix2[x,y] = 0
            else:
                pix2[x,y] = 255
    return new_img


def smooth(image):
    return image.filter(ImageFilter.SMOOTH)

def reduce_lines(image,color):
    new_img = image.copy()
    width, height = image.size
    pix = image.load()
    pix2 = new_img.load()
    for x in range(width):
        for y in range(height):
            if color == 0:
                if x+1 >= width or pix[x+1,y] < 127:
                    pix2[x,y] = color
                elif x-1 < 0 or pix[x-1,y] < 127:
                    pix2[x,y] = color
                elif y+1 >= height or pix[x,y+1] < 127:
                    pix2[x,y] = color
                elif y-1 < 0 or pix[x,y-1] < 127:
                    pix2[x,y] = color
            elif color == 255:
                if x+1 >= width or pix[x+1,y] > 127:
                    pix2[x,y] = color
                elif x-1 < 0 or pix[x-1,y] > 127:
                    pix2[x,y] = color
                elif y+1 >= height or pix[x,y+1] > 127:
                    pix2[x,y] = color
                elif y-1 < 0 or pix[x,y-1] > 127:
                    pix2[x,y] = color
            else:
                print 'Some undefined color. not black and not white: %d'%(color)

    return new_img

def thicken_lines(image):
    new_img = image.copy()
    width, height = image.size
    pix = image.load()
    pix2 = new_img.load()
    for x in range(width):
        for y in range(height):
            colors = []
            colors.append(_get(pix, image.size, (x+1,y)))
            colors.append(_get(pix, image.size, (x-1,y)))
            colors.append(_get(pix, image.size, (x,y+1)))
            colors.append(_get(pix, image.size, (x,y-1)))
            colors.append(_get(pix, image.size, (x+1,y+1)))
            colors.append(_get(pix, image.size, (x-1,y+1)))
            colors.append(_get(pix, image.size, (x+1,y-1)))
            colors.append(_get(pix, image.size, (x-1,y-1)))
            if any(map(lambda color: color > 20, colors)):
                pix2[x,y] = 255
    return new_img
