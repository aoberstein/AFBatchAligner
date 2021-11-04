#!/usr/bin/python3

from fatcat_functions_async import fatcatMultiProcess
import glob
from resultSummarization import *
from renderStructures import *

def main():
    
    ''' FATCAT BATCH ALIGNMENT '''
    # queryFiles = glob.glob("/home/adam/archive/intellij-workspace/test_area/db/" +
    #                        "FATCATdb_2021-10-22/*bFILT-30.0.pdb")

    queryFiles = glob.glob("/home/adam/projects/2021-11-01_U94_analysis/HHV6A_U1102_U94/" +
                            "ranked_0.pdb")

    FCJar = str("/home/adam/archive/intellij-workspace/aofatcat_project/out/artifacts/aofatcat.jar/" +
                      "aofatcat_project.jar")

    outDir = "/home/adam/projects/2021-11-01_U94_analysis/output"

    ### generate target list
    targetDir = "/home/adam/projects/2021-11-01_U94_analysis/FATCATdb_2021-11-02"
    files = glob.glob(targetDir + "/*.pdb")
    outList = open(targetDir + "/targetList.list", "w")
    for file in files:
        outList.write(file + "\n")
    outList.close()

    targetList = str(targetDir + "/targetList.list")


    for query in queryFiles:
        print(query)

        fatcatMultiProcess(
            queryPDB=query,
            targetPDBList=targetList,
            javaFullPath="/usr/bin/java",
            aoFatCatJar=FCJar,
            outputDir=outDir,
            alignmentCutoff=0.01,
            cores=32
        )


    pandasToXls('/home/adam/archive/intellij-workspace/test_area/pdb_test4_async/HCMV_TB40E-BAC_UL148_bFILT-30.0')

    ## batch summarize to xlsprocessing (multithreaded)
    pandasToXlsBatch(outputDirRoot=outDir, cores=32)


    ## batch pse and png export
    renderPdbBatch(outputDirRoot=outDir, cores=32)

if __name__ == '__main__':
    main()
    
    


