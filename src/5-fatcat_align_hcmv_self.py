#!/usr/bin/python3

from fatcat_functions import fatcatMultiProcess
from fatcat_functions import jFatCatAlign
import glob

def main():
    
    ''' FATCAT BATCH ALIGNMENT '''
    # files = glob.glob("/mnt/nvme_scratch/2021-10-04_fatcat_HCMV_self_to_self_run1/input/*b-FILT_30.0.pdb")
    queryFiles = glob.glob("/home/adam/archive/intellij-workspace/test_area/db/" +
                      "FATCATdb_2021-10-22/*UL148_bFILT-30.0.pdb")

    FCJar = str("/home/adam/archive/intellij-workspace/aofatcat_project/out/artifacts/aofatcat.jar/" +
                      "aofatcat_project.jar")

    targetList = str("/home/adam/archive/intellij-workspace/test_area/db/FATCATdb_2021-10-22/" +
                     "FATCAT_list_2021-10-22.list")

    outDir = "/home/adam/archive/intellij-workspace/test_area/" + \
            "output"


    for query in queryFiles:
        print(query)

        ## Test jFatCatAlign function
        # targets = glob.glob("/home/adam/archive/intellij-workspace/test_area/db/" +
        #                     "FATCATdb_2021-10-22/*_bFILT-30.0.pdb")
        # # target = targets[0]
        # for target in targets[0:50]:
        #     print(target)
        #     jFatCatAlign(query, target, "/usr/bin/java",
        #         "/home/adam/archive/intellij-workspace/aofatcat_project/out/" +
        #             "artifacts/aofatcat.jar/aofatcat_project.jar",
        #         "/home/adam/archive/intellij-workspace/test_area/output",
        #         "0.05"
        #     )


        fatcatMultiProcess(
            queryPDB=query,
            targetPDBList=targetList,
            javaFullPath="/usr/bin/java",
            aoFatCatJar=FCJar,
            outputDir="/home/adam/archive/intellij-workspace/test_area/output",
            alignmentCutoff=0.01,
            cores=8
        )

    
if __name__ == '__main__':
    main()
    
    


