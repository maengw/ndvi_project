#!/usr/bin/env python


import numpy as np
import cv2
import csv
from calibration import Calibrate


class CalculateIndex():
    
    # default filter_threshold is set to 0.2 because any objects(in pixels) lower than 0.2 are considered as non-plant.
    # I don't want to take non-plant objects into calculation for ndvi and gndvi.
    def __init__(self, cf, filter_threshold=0.2):

        # Only green, red, nir correction factors are required for ndvi and gndvi calculation
        # bcf = cf[0]
        self.gcf = cf[1]
        self.rcf = cf[2]
        self.nircf = cf[3]
        # recf = cf[4]
        self.filter_threshold = filter_threshold

    # update 3 channels image by multiplying their correction factor ( = calibration process)
    def update_img(self, g, r, nir):
        self.gimg = g[:,:,0] * self.gcf
        self.rimg = r[:,:,0] * self.rcf
        self.nirimg = nir[:,:,0] * self.nircf

    # NDVI = (NIR - R) / (NIR + R)
    # calculate average ndvi of leaves
    def calculate_ndvi(self):
        ndvi = np.divide((self.nirimg - self.rimg) , (self.nirimg + self.rimg))
        ndvi = ndvi.flatten()
        self.apply_filter(ndvi)

        ndvi_sum = np.sum(ndvi)
        nonzero_pix_num = np.count_nonzero(ndvi)
        avg_ndvi = ndvi_sum / nonzero_pix_num
        return avg_ndvi

    # GNDVI = (NIR - G) / (NIR + G)
    def calculate_gndvi(self):
        gndvi = np.divide((self.nirimg - self.gimg) , (self.nirimg + self.gimg))
        gndvi = gndvi.flatten()
        self.apply_filter(gndvi)
        
        gndvi_sum = np.sum(gndvi)
        nonzero_pix_num = np.count_nonzero(gndvi)
        avg_gndvi = gndvi_sum / nonzero_pix_num
        return avg_gndvi

    # change values that are smaller than threshold to 0.
    def apply_filter(self,aray):
        aray[aray<self.filter_threshold] = 0


if __name__ == "__main__":

    # image 86 are calibration pannel images.
    bcrpimg = '/home/woo/PycharmProjects/immlproject/aligned_data/000/FIMG_0086_1.tif'
    gcrpimg = '/home/woo/PycharmProjects/immlproject/aligned_data/000/FIMG_0086_2.tif'
    rcrpimg = '/home/woo/PycharmProjects/immlproject/aligned_data/000/FIMG_0086_3.tif'
    nircrpimg = '/home/woo/PycharmProjects/immlproject/aligned_data/000/FIMG_0086_4.tif'
    recrpimg = '/home/woo/PycharmProjects/immlproject/aligned_data/000/FIMG_0086_5.tif'

    CALI = Calibrate()
    CALI.update_avg_crp(bcrpimg)
    bcf = CALI.correct()

    CALI.update_avg_crp(gcrpimg)
    gcf = CALI.correct()

    CALI.update_avg_crp(rcrpimg)
    rcf = CALI.correct()

    CALI.update_avg_crp(nircrpimg)
    nircf = CALI.correct()

    CALI.update_avg_crp(recrpimg)
    recf = CALI.correct()

    cf = [bcf, gcf, rcf, nircf, recf]


    # g
    # img2 = cv2.imread('/home/woo/PycharmProjects/immlproject/aligned_data/000/FIMG_000%s_2.tif')
    img2 = cv2.imread('/home/woo/PycharmProjects/immlproject/aligned_data/000/FIMG_0000_2.tif')

    # r
    img3 = cv2.imread('/home/woo/PycharmProjects/immlproject/aligned_data/000/FIMG_0000_3.tif')

    # nir
    img4 = cv2.imread('/home/woo/PycharmProjects/immlproject/aligned_data/000/FIMG_0000_4.tif')

    CI = CalculateIndex(cf)
    CI.update_img(img2, img3, img4)
    ndvi = CI.calculate_ndvi()
    gndvi = CI.calculate_gndvi()
    # print(ndvi)
    # print(gndvi)


