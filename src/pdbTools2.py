def checkFolderBackslash(Dir):
    import re
    if re.match(".*[/]$", Dir):
        # print("FOUND:" + Dir)
        return Dir
    else:
        # print("ADDING BACKSLASH:" + Dir)
        return Dir + "/"


def exportPdbToLengths(dbFolder, cores = 32):
    '''
    input a folder of single chain pdb files (i.e. "a formatted db folder)
    This function will only work on single chain pdbs!
    '''

    import os, sys, glob, time
    import multiprocess as mp
    from multiprocess import Manager
    from Bio.PDB.PDBParser import PDBParser
    from Bio.PDB.PDBIO import PDBIO
    from Bio.PDB.PDBIO import Select

    if cores >= int(mp.cpu_count()):
        optCores = int(mp.cpu_count())-1
        # print("Too many cores selected")
        # print("Reducing to " + str(optCores) + " cores")
        cores = optCores
    if cores < int(mp.cpu_count()):
        cores = cores

    ## make sure folder has trailing slash
    dbFolder = checkFolderBackslash(dbFolder)

    ### create output file
    outName = dbFolder + "pdbToLengthsTable.tsv"
    outFile = open(outName, "w")

    pdbFiles = glob.glob(dbFolder + "*.pdb")
    print(pdbFiles)
    ts = time.time()

    batchDict = {}
    b = 1
    for i in range(0, len(pdbFiles), cores):
        batchName = "b"+str(b)
        batchDict[batchName] = pdbFiles[i:i + cores]
        b = b + 1
    print(batchDict)

    ## make sure folder has trailing slash
    dbFolder = checkFolderBackslash(dbFolder)

    ### create output file
    outName = dbFolder + "pdbToLengthsTable.tsv"
    outFile = open(outName, "w")

    ### create output subdirectories
    # query = os.basename(queryPDB)
    queryPrefix = os.path.basename(queryPDB).rstrip(".pdb")
    subDir = outputDir+"/"+queryPrefix
    if os.path.exists(subDir):
        pass
    else:
        os.mkdir(subDir, mode = 0o755)

    ts = time.time()
    ### multiprocess with fatcat
    for key, values in batchDict.items():
        print("[renderPdbBatch]: Processing batch ", key, " of ", len(batchDict))
        procs = []
        # if key == "b1":
        #     print(key, values)
        with open(os.devnull, 'w') as devnull:
            # suppress stdout
            orig_stdout_fno = os.dup(sys.stdout.fileno())
            os.dup2(devnull.fileno(), 1)
            # suppress stderr
            orig_stderr_fno = os.dup(sys.stderr.fileno())
            os.dup2(devnull.fileno(), 2)
            # if key == "b1" or key == "b2" or key == "b3":
            if key inc ["b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9", "b10"]:
                for targetPDB in values:
                    targetPDB = targetPDB.strip()
                    # print(targetPDB)
                    p = mp.Process(target=jFatCatAlign,
                                   args=(queryPDB, targetPDB, javaFullPath, aoFatCatJar,
                                         subDir, alignmentCutoff))
                    procs.append(p)
                    # print(procs)
                    p.start()
                for proc in procs:
                    proc.join()
        os.dup2(orig_stdout_fno, 1)  # restore stdout
        os.dup2(orig_stderr_fno, 2)  # restore stderr
    print('Time in batch parallel:', time.time() - ts)