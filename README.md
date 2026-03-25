# Align alphafold predicitons using biojava fatcat-flexible aligner

1) download pdb db to local directory
    downloadPdbDB.downloadPdbDB

2) format PDB
    formatPdbDB.formatPDB_db(dbLocation=dbRoot, cores=32)
    a) extract each file to a working directory
    b) extract each chain of each pdb file or add "_A" suffix to single chain pdbs
    c) write chain (filePath) to length conversion table

4) TO DO: download PDB cluster files
    downloadPdbClusters.downloadPdbClusters(Dir)

5) extract PDB clusters (create list of first pdb in each cluster and append path of
    local pdb database to each pdb)
    formatPdbClusters.extractPdbClusters(clusterFile, dbDir)

6) length filter an extracted pdb cluster file (reduce search space)
    formatPdbClusters.lengthFilter(clusterList, lengthToPdbTSV, maxLength)

6.5) check cluster for duplicates and remove
    formatPdbClusters.checkDups(PdbListFile)
    formatPdbClusters.removeDups(PdbListFile)

7) Batch align using fatCat
    dependency = aofatcat.jar
    AlignFatcatFlex.fatcatMultiProcess(
        queryPDB=query,
        targetPDBList=targetList,
        javaFullPath="/usr/bin/java",
        aoFatCatJar=FCJar,
        outputDir=outDir,
        alignmentCutoff=0.01,
        cores=32
    )

8) Aggregate fatCat results to excel and pymol .pse files

    ## batch summarize to xls (multithreaded)
    resultSummarization.pandasToXlsBatch(outputDirRoot=outDir, cores=32)

    ## batch pse
    renderStructures.renderPdbBatch(outputDirRoot=outDir, cores=32)
