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
    output a tab delimited conversion table ([full pdb path] [chain id] [length])
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

    ### define target files
    pdbFiles = glob.glob(dbFolder + "*.pdb")
    print(pdbFiles)

    ### create batch dict
    batchDict = {}
    b = 1
    for i in range(0, len(pdbFiles), cores):
        batchName = "b"+str(b)
        batchDict[batchName] = pdbFiles[i:i + cores]
        b = b + 1
    print(batchDict)

    ### start timer
    ts = time.time()

    def getLength(pdbFile):
        id = os.path.basename(pdbFile).rstrip(".pdb")
        print(id)
        ### ths following if/esle
        if PDBParser().get_structure(id, pdbFile):
            structure = PDBParser().get_structure(id, pdbFile)
            if (len(list(structure.get_chains()))) > 1:
                print("ERROR: found pdb with more than 1 chain")
                length = "NA"
            else:
                chain = list(structure.get_chains())[0]
            length = len(list(chain.get_residues()))
            chain_id = chain.id
            # print(pdbFile + "\t" + chain.id + "\t" + str(length))
            return(pdbFile + "\t" + chain.id + "\t" + str(length))
        else:
            return

    ### multiprocess batches
    p = mp.Pool(cores)
    for key, values in batchDict.items():
        print("[exportPdbToLengths]: Processing batch ", key, " of ", len(batchDict))
        procs = []
        # if key == "b1":
        #     print(key, values)
        # with open(os.devnull, 'w') as devnull:
        #     # suppress stdout
        #     orig_stdout_fno = os.dup(sys.stdout.fileno())
        #     os.dup2(devnull.fileno(), 1)
        #     # suppress stderr
        #     orig_stderr_fno = os.dup(sys.stderr.fileno())
        #     os.dup2(devnull.fileno(), 2)
        if key:
            for result in p.imap(getLength, values):
                # print(result)
                outFile.write(result + "\n")




        # os.dup2(orig_stdout_fno, 1)  # restore stdout
        # os.dup2(orig_stderr_fno, 2)  # restore stderr
    print('Time in batch parallel:', time.time() - ts)
    outFile.close()