#!/usr/bin/python3

from fatcat_functions import fatcatMultiProcess
from fatcat_functions import jFatCatAlign
import glob
from resultSummarization import *
from renderStructures import *

def main():
    
    ''' FATCAT BATCH ALIGNMENT '''
    # queryFiles = glob.glob("/home/adam/archive/intellij-workspace/test_area/db/" +
    #                        "FATCATdb_2021-10-22/*bFILT-30.0.pdb")

    queryFiles = glob.glob("/home/adam/archive/intellij-workspace/test_area/db/" +
                            "FATCATdb_2021-10-22/*UL148_bFILT-30.0.pdb")

    FCJar = str("/home/adam/archive/intellij-workspace/aofatcat_project/out/artifacts/aofatcat.jar/" +
                      "aofatcat_project.jar")

    targetList = str("/home/adam/archive/intellij-workspace/test_area/FATCATdb_2021-10-26/" +
                     "FATCAT_list_2021-10-26.list")

    outDir = "/home/adam/archive/intellij-workspace/test_area/pdb_test1"


    for query in queryFiles:
        print(query)

        # fatcatMultiProcess(
        #     queryPDB=query,
        #     targetPDBList=targetList,
        #     javaFullPath="/usr/bin/java",
        #     aoFatCatJar=FCJar,
        #     outputDir=outDir,
        #     alignmentCutoff=0.01,
        #     cores=7
        # )


        # pandasToXls('/home/adam/archive/intellij-workspace/test_area/pdb_test1/HCMV_TB40E-BAC_UL148_bFILT-30.0')

        # ## batch summarize to xlsprocessing (multithreaded)
        pandasToXlsBatch(outputDirRoot=outDir, cores=8)


        # ## batch pse and png export
        renderPdbBatch(outputDirRoot=outDir, cores=8)

if __name__ == '__main__':
    main()
    
    


