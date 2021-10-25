#!/usr/bin/python3

from resultSummarization import *

def main():

    # ## process a single "fcWriteTemp" dir
    # dir = "/home/adam/archive/intellij-workspace/test_area/output/HCMV_TB40E-BAC_UL138_bFILT-30.0"
    # # FCtoXls(dir)
    # pandasToXls(dir)

    ## batch processing (multithreaded)
    outputDirRoot = "/home/adam/archive/intellij-workspace/test_area/output/"
    catFatcatTempFilesBatch(outputDirRoot=outputDirRoot, cores=8)





if __name__ == '__main__':
    main()



