#!/usr/bin/env python


import numpy as np
import cv2



x = 0
y = 36
w = 1238
h = 940

class AlignImages():
    # IMG_XXXX_1.tif : Blue channel image
    # IMG_XXXX_2.tif : Green channel image
    # IMG_XXXX_3.tif : Red channel image
    # IMG_XXXX_4.tif : NearInfraRed(NIR) channel image
    # IMG_XXXX.5.tif : RedEdge channel image
    # The images are all 3d, but the values in all channels are the same.


    # Constructor
    def __init__(self, B2RE=(-12, -20), G2RE=(-42, 10), R2RE=(-23, 36), NIR2RE=(-3, 32)):
        # Params = (x, y) are the amount of displacement in pixels from the RedEdge channel image(as RedEdge cam is in the center).
        # basically the amount of pixels I want to slide in (x,y) direction. (e.g. B2RE=(-12, -20) means shift Blue channel image by -12 in x direction and -20 in y direction
        #                                                                                                 then it will be aligned with RedEdge channel image
        self.B2RE = B2RE
        self.G2RE = G2RE
        self.R2RE = R2RE
        self.NIR2RE = NIR2RE
        self.RE2RE = (0, 0)

        # Need to crop image after sliding since we want all the images from channels to be the same size
        # (x,y) will be the upper left corner of new image size and w,h are width and height
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        # zeros_image=np.zeros(shape=( (self.h - self.y), (self.w - self.x), 3))
        # (904, 1238, 3)

    # calculate sliding factor; tf is how much we wanna slide in (x,y) form
    def get_translation_factor(self, tf):
        return np.float32([ [1, 0, tf[0]], [0, 1, tf[1]] ])

    # func to slide image
    def translate(self,read_img, translation_factor):
        (rows, cols) = read_img.shape[:2]
        res = cv2.warpAffine(read_img, translation_factor, (cols, rows))
        return res

    # check which channel image is read then complete translating image and return it
    def complete_translate(self, img_filename):
        if '1.' in img_filename:
            translation_factor = self.get_translation_factor(self.B2RE)
        elif '2.' in img_filename:
            translation_factor = self.get_translation_factor(self.G2RE)
        elif '3.' in img_filename:
            translation_factor = self.get_translation_factor(self.R2RE)
        elif '4.' in img_filename:
            translation_factor = self.get_translation_factor(self.NIR2RE)
        else:
            translation_factor = self.get_translation_factor(self.RE2RE)

        img = cv2.imread(img_filename)
        translated_img = self.translate(img, translation_factor)
        return translated_img

    # crop image for new size
    def crop_img(self, read_img):
        self.cropped_img = read_img[self.y:self.h, self.x:self.w]
        return self.cropped_img

    # concatenate b,g,r channels for visualization. Not necessary for the purpose of this project as they are not used to calculate NDVI, GNDVI. 
    def make_bgr_img(self, b_img, g_img, r_img):
        return np.dstack( (b_img[:,:,0], np.dstack( (g_img[:,:,0], r_img[:,:,0]) )) )



if __name__ == "__main__":
    # sample images
    blue_img = '/home/woo/PycharmProjects/immlproject/data/000/IMG_0050_1.tif'
    green_img = '/home/woo/PycharmProjects/immlproject/data/000/IMG_0050_2.tif'
    red_img = '/home/woo/PycharmProjects/immlproject/data/000/IMG_0050_3.tif'
    nir_img = '/home/woo/PycharmProjects/immlproject/data/000/IMG_0050_4.tif'
    re_img = '/home/woo/PycharmProjects/immlproject/data/000/IMG_0050_5.tif'

    AI = AlignImages()
    translated_bimg = AI.complete_translate(blue_img)
    cropped_bimg = AI.crop_img(translated_bimg)

    translated_gimg = AI.complete_translate(green_img)
    cropped_gimg = AI.crop_img(translated_gimg)

    translated_rimg = AI.complete_translate(red_img)
    cropped_rimg = AI.crop_img(translated_rimg)
    bgr_img = AI.make_bgr_img(cropped_bimg, cropped_gimg, cropped_rimg)

    cv2.imshow("bgr image", bgr_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
