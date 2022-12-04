#!/usr/bin/env python


import numpy as np
import cv2


class Calibrate():


    # Panel Reflectance Value(PRV) = approx. 0.6 ; given by Micasense manufacturer
    # Correction Factor(CF) = PRV * 255 / est.PRV ( i.e. average crp)
    # Need to multiply CF to NIR and R images for calibration


    # CRP(Calibration Reflectance Pannel): A white board that is used for calibration. Theoretically all the pixels in image of panel 
    #                                      are 255, but in real it is not due to sunlight and many other reasons. So we calibrate using this.


    def __init__(self, bcrp=(525,800,311,563), gcrp = (530,800,338,595), rcrp = (530,800,338,595), nircrp = (510, 780,300,560), recrp = (520, 790,320, 580),
                       bprv=0.6177, gprv=0.6284, rprv=0.6317, nirprv=0.6045, reprv=0.6276):
                       # default panel reflectance value provided by Micasense.

        """Constructor
        @param crp - coordinates of upper left and lower right corners of calibration reflectance panel (x1, x2, y1, y2)
        @param prv - panel reflectance value which is a number given by manufacturer for calibration process
        """

        self.bcrp = bcrp
        self.gcrp = gcrp
        self.rcrp = rcrp
        self.nircrp = nircrp
        self.recrp = recrp

        self.bprv = bprv
        self.gprv = gprv
        self.rprv = rprv
        self.nirprv = nirprv
        self.reprv = reprv
        self.prv = 0

    # Change corner coordinates of calibration panels. only needed when using different company's multispectral camera or other model of micasense's
    def change_crp(self,channel):
        cmd = input(" Please type in the coordinates of calibration panel in (x1,x2,y1,y2) format\n")
        cmd = int(cmd)
        if channel == 'b':
            self.bcrp = cmd
        elif channel == 'g':
            self.gcrp = cmd
        elif channel == 'r':
            self.rcrp = cmd
        elif channel == 'nir':
            self.nircrp = cmd
        elif channel == 're':
            self.recrp = cmd

    # Change prv. only needed when using different company's multispectral camera or other model of micasense's
    def change_prv(self, channel):
        cmd = input("Please type in the prv provided by manufacturer\n")
        cmd = float(cmd)
        if channel == 'b':
            self.bprv = cmd
        elif channel == 'g':
            self.gprv = cmd
        elif channel == 'r':
            self.rprv = cmd
        elif channel == 'nir':
            self.nirprv = cmd
        elif channel == 're':
            self.reprv = cmd
        
    # check which channel image is being read and update manufacturer provided prv and estimated prv(avg_crp)
    def update_avg_crp(self, cali_panel_img):
        if '1.' in cali_panel_img:
            crp_img = cv2.imread(cali_panel_img)[self.bcrp[0]:self.bcrp[1], self.bcrp[2]:self.bcrp[3], 0]
            self.prv = self.bprv

        elif '2.' in cali_panel_img:
            crp_img = cv2.imread(cali_panel_img)[self.gcrp[0]:self.gcrp[1], self.gcrp[2]:self.gcrp[3], 0]
            self.prv = self.gprv        

        elif '3.' in cali_panel_img:
            crp_img = cv2.imread(cali_panel_img)[self.rcrp[0]:self.rcrp[1], self.rcrp[2]:self.rcrp[3], 0]
            self.prv = self.rprv        

        elif '4.' in cali_panel_img:
            crp_img = cv2.imread(cali_panel_img)[self.nircrp[0]:self.nircrp[1], self.nircrp[2]:self.nircrp[3], 0]
            self.prv = self.nirprv

        elif '5.' in cali_panel_img:
            crp_img = cv2.imread(cali_panel_img)[self.recrp[0]:self.recrp[1], self.recrp[2]:self.recrp[3], 0]
            self.prv = self.reprv        

        self.avg_crp = np.sum(crp_img) / np.size(crp_img)

    # calculate correction factor
    def correct(self):
        self.corrector = self.prv * 255
        self.cf = self.corrector / self.avg_crp
        return self.cf



if __name__ == "__main__":
    # calibration images
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


    print(bcf)
    print(gcf)
    print(rcf)
    print(nircf)
    print(recf)

