#!/usr/bin/env python


import numpy as np
import cv2
import csv
import os
from natsort import natsorted
from calibration import Calibrate
from process_multi_images import AlignImages
from calc_ndvi import CalculateIndex


def main():

    CA = Calibrate()
    # calibration panel images
    # need to calibrate images when calculating ndvi and gndvi
    # change calipanel_path to where your calibration panel images are.
    calipanel_path = '/home/woo/Desktop/ndvi_project/data/calibration_panel/' 
    bcrpimg =  os.path.join(calipanel_path, 'FIMG_0086_1.tif')
    gcrpimg =  os.path.join(calipanel_path, 'FIMG_0086_2.tif')
    rcrpimg =  os.path.join(calipanel_path, 'FIMG_0086_3.tif')
    nircrpimg =  os.path.join(calipanel_path, 'FIMG_0086_4.tif')
    recrpimg =  os.path.join(calipanel_path, 'FIMG_0086_5.tif')

    # update average(estimated) calibration reflectance panel 
    CA.update_avg_crp(bcrpimg)
    # get calculate correction factor for each channel images
    bcf = CA.correct()

    CA.update_avg_crp(gcrpimg)
    gcf = CA.correct()

    CA.update_avg_crp(rcrpimg)
    rcf = CA.correct()

    CA.update_avg_crp(nircrpimg)
    nircf = CA.correct()

    CA.update_avg_crp(recrpimg)
    recf = CA.correct()

    # correction factors for calibration when calculating ndvi and gndvi
    cf = [bcf, gcf, rcf, nircf, recf]


    AI = AlignImages()
    CI = CalculateIndex(cf)

    img2 = None
    img3 = None
    img4 = None

    ndvi_list = []
    gndvi_list = []

    # path to all tif images
    # img_path = '/home/woo/PycharmProjects/immlproject/data/000/'

    # sample leaves images
    # change img_path to where your data are
    img_path = '/home/woo/Desktop/ndvi_project/data/leaves_data/'
    # sort files in directory
    files_to_read = natsorted(os.listdir(img_path))


    checker = True
    for a_file in files_to_read:
        # when the image is green channel image
        if checker == True and '_2' in a_file:
            img2 = os.path.join(img_path, a_file)
            # translate blue channel image
            img2 = AI.complete_translate(img2)
            # crop an image
            img2 = AI.crop_img(img2)
            # translated_gimg = AI.complete_translate(img2)
            # cropped_gimg = AI.crop_img(translated_gimg)

        elif checker == True and '_3' in a_file:
            img3 = os.path.join(img_path, a_file)
            img3 = AI.complete_translate(img3)
            img3 = AI.crop_img(img3)
            # translated_rimg = AI.complete_translate(img3)
            # cropped_rimg = AI.crop_img(translated_rimg)

        elif checker == True and '_4' in a_file:
            img4 = os.path.join(img_path, a_file)
            img4 = AI.complete_translate(img4)
            img4 = AI.crop_img(img4)
            # translated_nirimg = AI.complete_translate(img4)
            # cropped_nirimg = AI.crop_img(translated_nirimg)

            # we only need channel green, red, nir images to calculate ndvi and gndvi; make it go into next if statement for calculation
            checker = False

        if checker == False:
            # apply calibration on g,r,nir images and update
            CI.update_img(img2, img3, img4)
            ndvi = CI.calculate_ndvi()
            gndvi = CI.calculate_gndvi()
            ndvi_list.append(ndvi)
            gndvi_list.append(gndvi)
            checker = True

    header = ['ndvi', 'gndvi']
    # change directory to where you want to save ndvi and gndvi
    with open("/home/woo/Desktop/ndvi_project/result/ndvi_gndvi_leaves.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(len(ndvi_list)):
            writer.writerow([ndvi_list[i], gndvi_list[i]])


if __name__ == "__main__":
    main()
