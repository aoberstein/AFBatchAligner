#!/usr/bin/python3

from fatcat_functions_async import fatcatMultiProcess
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

    outDir = "/home/adam/archive/intellij-workspace/test_area/test6_async_lengthFilt_bc40"

    targetList = str("/home/adam/archive/db/pdb/2021-10-26/pdb_clusters/bc-40_filt80.list")


    for query in queryFiles:
        print(query)

        fatcatMultiProcess(
            queryPDB=query,
            targetPDBList=targetList,
            javaFullPath="/usr/bin/java",
            aoFatCatJar=FCJar,
            outputDir=outDir,
            alignmentCutoff=0.001,
            cores=32
        )


    # pandasToXls('/home/adam/archive/intellij-workspace/test_area/pdb_test4_async/HCMV_TB40E-BAC_UL148_bFILT-30.0')

    ## batch summarize to xlsprocessing (multithreaded)
    pandasToXlsBatch(outputDirRoot=outDir, cores=32)

    ## batch pse and png export
    renderPdbBatch(outputDirRoot=outDir, cores=32)

if __name__ == '__main__':
    main()
    
    


