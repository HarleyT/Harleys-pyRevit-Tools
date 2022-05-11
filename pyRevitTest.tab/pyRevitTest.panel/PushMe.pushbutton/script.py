# pyRevit metadata
__title__ = "File Info"
__author__ = "Harley Trappitt"

import os
filename = "C:/Users/htrappitt/ACCDocs/GHD Services Pty Ltd/12545014 - AML Detail Design 15MTPA/Project Files/02 - DELIVERY/_REFERENCES SHARED/3470-134-MDL-CV-0046.nwc"
statbuff = os.stat(filename)
print("Modification time: {}".format(statbuff.st_mtime))