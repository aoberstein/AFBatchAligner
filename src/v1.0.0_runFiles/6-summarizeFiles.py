#!/usr/bin/python3

from resultSummarization import *
from renderStructures import *

def main():

    # ## process a single "fcWriteTemp" dir
    # dir = "/home/adam/archive/intellij-workspace/test_area/output/HCMV_TB40E-BAC_UL138_bFILT-30.0"
    # # FCtoXls(dir)
    # pandasToXls(dir)

    # ## batch processing (multithreaded)
    # outputDirRoot = "/home/adam/archive/intellij-workspace/test_area/output/"
    # catFatcatTempFilesBatch(outputDirRoot=outputDirRoot, cores=8)

    # ##
    # pdb = "/home/adam/archive/intellij-workspace/test_area/output/HCMV_TB40E-BAC_UL148_bFILT-30.0" + \
    #       "/HCMV_TB40E-BAC_UL148_bFILT-30.0_HCMV_TB40E-BAC_RL10_alignment.pdb"
    # renderPDB(inputPDB=pdb)

    ## batch pse and png export
    outputDirRoot = "/home/adam/archive/intellij-workspace/test_area/output/"
    renderPdbBatch(outputDirRoot=outputDirRoot, cores=8)



if __name__ == '__main__':
    main()



