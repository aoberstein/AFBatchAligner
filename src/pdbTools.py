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
    ts = time.time()

    pool = mp.Pool(processes=cores)
    manager = Manager()
    lineDict = manager.dict()
    # lineList = []
    # lineDict = {}

    def getPdbLength(d, pdbFile, chain_id, length):
        d[pdbFile] = [chain_id,length]

    for pdbFile in pdbFiles:
        id = os.path.basename(pdbFile).rstrip(".pdb")
        structure = PDBParser().get_structure(id, pdbFile)
        if (len(list(structure.get_chains()))) > 1:
            print("ERROR: found pdb with more than 1 chain")
            length = "NA"
        else:
            chain = list(structure.get_chains())[0]
        length = len(list(chain.get_residues()))
        chain_id = chain.id
        print(pdbFile + "\t" + chain.id + "\t" + str(length))

        pool.apply_async(func=getPdbLength, args=(lineDict, pdbFile, chain_id, length))
    pool.close()
    pool.join()

    print('Time in parallel:', time.time() - ts)
    # print(lineDict)
    for key, value in lineDict.items():
        print(key, value)
        file = key
        chain = value[0]
        length = value[1]
        outFile.write("%1s\t%2s\t%3s\n" % (file, chain, length))
    outFile.close()

