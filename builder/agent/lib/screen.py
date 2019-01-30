# Date: 08/13/2018
# Author: Pure-L0G1C
# Description: Screen shot

from mss import mss
from time import time 
from .const import ScreenConst
from os import path, mkdir, remove, listdir


class Screenshot:

    def __init__(self):
        self.img_num = 0
        self.img = path.join(ScreenConst.DIR.value, ScreenConst.IMG.value)

        if not path.exists(ScreenConst.DIR.value):
            mkdir(ScreenConst.DIR.value)
        else:
            self.remove_images()
    
    def capture_img(self):
        img = None         

        while True:
            self.img_num += 1
            img = '{}{}{}'.format(self.img, self.img_num, ScreenConst.EXTEN.value)

            if not path.exists(img):
                break 

        with mss() as sct:
            sct.shot(mon=-1, output=img)
        
    def remove_images(self):
        self.img_num = 0

        for img in listdir(ScreenConst.DIR.value):
            img = path.join(ScreenConst.DIR.value, img)
            
            if path.exists(img):
                try:
                    remove(img)
                except:
                    pass 