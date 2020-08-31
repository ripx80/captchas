#!/usr/bin/python
'''

Captcha Breaker

1. Get the Image,CaptchaID,CSRF Token
2. Clean the Image (Convert to GIF (easier since it has 255 colours )/ Filters)
4. Find the caligraphic method (Text Art)
3. Try some Algorythms to find the right text
4. Check the Results and use the highly rated (Algro rating)
5. Send the Text Response
6. Check the Response from Captcha Server (T/F)
7. Save the Result in DB (AI)

http://www.boyter.org/decoding-captchas/

http://scikit-learn.org/stable/
http://rafael.kontesti.me/blog/posts/Breaking_a_captcha/
http://www.dc949.org/projects/stiltwalker/
http://www.teknoids.net/content/hacking-and-defeating-googles-recaptcha-99-accuracy

Needed :
tesseract-ocr
Python-Tesseract


1. Tesseract
2. app-text/gocr
3. app-text/ocrad
4. dev-python/pyocr

http://www.google.com/recaptcha/demo/

'''

from PIL import Image,ImageEnhance
from operator import itemgetter
from pytesseract import image_to_string


from splitter import Picture

#image=Picture('capts/captcha.jpg')

#image.printVector(50)

cap_img='capts/captcha.jpg'
#cap_gif='tmp/captcha.gif'

#check if it is a gif.
img=Image.open(cap_img)

'only 255 colors :-)'
#img = img.convert("P")
img = img.convert('P')
img2 = Image.new("P",img.size,255)
#img = img.convert("P")

temp = {}

for x in range(img.size[1]):
  for y in range(img.size[0]):
    pix = img.getpixel((y,x))
    temp[pix] = pix
    if pix == 0 or pix == 255: # these are the numbers to get
      img2.putpixel((y,x),0)



#~ nx, ny = img2.size
#~ img2 = img.resize((int(nx*5), int(ny*5)), Image.BICUBIC)
#~ enh=ImageEnhance.Contrast(img2)
#~ enh.enhance(1.3)

#img2.save("output.gif")

# new code starts here

inletter = False
foundletter=False
start = 0
end = 0

letters = []

for y in range(img2.size[0]): # slice across
    for x in range(img2.size[1]): # slice down
        pix = img2.getpixel((y,x))
        if pix != 255:
            inletter = True

        if foundletter == False and inletter == True:
            foundletter = True
            start = y

        if foundletter == True and inletter == False:
            foundletter = False
            end = y
            letters.append((start,end))

        inletter=False
print(letters)


#find the using colors
#~ his=img.histogram()
#~ values = {}
#~ for i in range(256):
  #~ values[i] = his[i]
#~ for j,k in sorted(values.items(), key=itemgetter(1), reverse=True)[:10]:
  #~ print(j,k)


