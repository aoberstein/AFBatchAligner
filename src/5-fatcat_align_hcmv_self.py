#!/usr/bin/python3

from fatcat_functions import fatcatMultiProcess
from fatcat_functions import jFatCatAlign
import glob

def main():
    
    ''' FATCAT BATCH ALIGNMENT '''
    # files = glob.glob("/mnt/nvme_scratch/2021-10-04_fatcat_HCMV_self_to_self_run1/input/*b-FILT_30.0.pdb")
    files = glob.glob("/home/adam/archive/intellij-workspace/test_area/db/" +
                      "FATCATdb_2021-10-22/*UL148_bFILT-30.0.pdb")
    for file in files:
        query = file
        print(query)
        
        targetList = str("/home/adam/archive/intellij-workspace/test_area/db/FATCATdb_2021-10-22/" +
                         "FATCAT_list_2021-10-22.list")

        aoFatcatJar = str("/home/adam/archive/intellij-workspace/aofatcat_project/out/artifacts/aofatcat.jar/" +
                          "aofatcat_project.jar")

        outDir = "/home/adam/archive/intellij-workspace/test_area/" + \
                 "output"
        targets = glob.glob("/home/adam/archive/intellij-workspace/test_area/db/" +
                            "FATCATdb_2021-10-22/*_bFILT-30.0.pdb")
        # target = targets[0]
        for target in targets[0:10]:
            print(target)
            jFatCatAlign(query, target, "/usr/bin/java",
                "/home/adam/archive/intellij-workspace/aofatcat_project/out/" +
                    "artifacts/aofatcat.jar/aofatcat_project.jar",
                "/home/adam/archive/intellij-workspace/test_area/output",
                "0.05"
            )


        # fatcatMultiProcess(query, targetList, fatcatDir, outDir, 0.2, 30)

    
if __name__ == '__main__':
    main()
    
    


