
from PIL import Image
from emailSenderWidget import *

class ImageHandler:

    def __init__(self, range):
        self.range = range
        self.black = [0, 0, 0, 255]
        self.white = [255, 255, 255, 255]
        self.trasparent = (255, 255, 255, 0) # not vector

    def remove_background(self, im, color, processedName):
        # http://stackoverflow.com/questions/21217384/remove-background-colour-from-image-using-python-pil
        # http://stackoverflow.com/questions/765736/using-pil-to-make-all-white-pixels-transparent
        self.im = im.convert('RGBA')
        self.data = im.getdata()

        newData = []
        avColor = self.color_average(im)
        for item in self.data:
            # if self.is_in_range(item[0], color[0], self.range) and self.is_in_range(item[1], color[1], self.range) and self.is_in_range(item[2], color[2], self.range):
            if (self.dist(item[0], item[1], item[2], avColor[0], avColor[1], avColor[2]) < self.range):
                newData.append(self.trasparent)
            else:
                newData.append(item)
        self.im.putdata(newData)
        self.save_image(self.im, 'transparent-' + processedName, "PNG")

    def color_average(self, im):
        firula = 30
        r = 0
        g = 0
        b = 0
        bg_w, bg_h = self.im.size
        img = im.convert('RGB')
        rangge = bg_w/firula
        d=0
        for i in range(0, firula):
            x, y, z = img.getpixel((d, 1))
            d += rangge
            r += x;g += y;b += z
        return r/firula, g/firula, b/firula


    def put_background(self, background, processedName):
        # http://stackoverflow.com/questions/13637028/adding-a-background-image-in-python
        # http://stackoverflow.com/questions/2563822/how-do-you-composite-an-image-onto-another-image-with-pil-in-python
        background = background.convert('RGBA')
        im_w, im_h = self.im.size
        bg_w, bg_h = background.size
        offset = ((bg_w - im_w) / 2, (bg_h - im_h) / 2)
        # http://stackoverflow.com/questions/5324647/how-to-merge-a-transparent-png-image-with-another-image-using-pil
        background.paste(self.im, offset, self.im)
        background = self.put_logo(background)
        self.save_image(background, 'implusback-' + processedName, "PNG")
        # self.show_image('implusback-'+processedName)

    def put_logo(self, i):
        i = i.convert('RGB')
        bg_w, bg_h = i.size
        logo = Image.open("images/inputs/logos/logo-eco-itaipu.png")
        logo = logo.convert('RGBA')
        logo_w, logo_h = logo.size

        offset = ((bg_w - logo_w - 20), (bg_h - logo_h - 20))
        # http://stackoverflow.com/questions/5324647/how-to-merge-a-transparent-png-image-with-another-image-using-pil
        i.paste(logo, offset, logo)

        logo1 = Image.open("images/inputs/logos/eco-1-gray.png")
        logo1.convert("RGBA")
        offset = (20, 20)
        i.paste(logo1, offset, logo1)

        return i

    def dist(self, x0, y0, z0, x1, y1, z1):
        import math
        a = (x1 - x0)**2 + (y1 - y0)**2 + (z1 - z0)**2
        b = math.sqrt(a)
        # print b
        return b

    def is_in_range(self, item, val, tolerance):
        if item > (val - tolerance) and item < (val + tolerance):
            return True
        else:
            return False

    def save_image(self, i, name, type):
        # print type
        i.save("images/outputs/"+name, type)

    def show_image(self,path):
        self.windowImg = EmailSenderWidget('images/outputs/'+path)
