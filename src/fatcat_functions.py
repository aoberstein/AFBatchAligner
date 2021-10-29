##
##
###### functions #################################################

def filterPDB(file, cutoff):
    ### see: https://biopython-cn.readthedocs.io/zh_CN/latest/en/chr11.html
    ### or: http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec182
    from Bio.PDB.PDBParser import PDBParser
    from Bio.PDB.PDBIO import PDBIO
    import os
    
    #custom select
    class Select():
        def accept_model(self, model):
            return True
        def accept_chain(self, chain):
            return True
        def accept_residue(self, residue):
            return True       
        def accept_atom(self, atom):
            # print("atom id:" + atom.get_id())
            # print("atom name:" + atom.get_name())
            if atom.get_bfactor() >= cutoff:  
                # print("True") 
                return True
            else:
                # print("Filtering: "+atom.get_id(), atom.get_bfactor(),
                # atom.get_parent())
                return False

    id = os.path.basename(file).rstrip(".pdb")
    outPrefix = file.rstrip(".pdb")+"_bFILT-"+str(cutoff)+".pdb"
    # print("[OUTPUT]: "+outPrefix)
    pdb = PDBParser().get_structure(id, file)
    io = PDBIO()
    io.set_structure(pdb)
    io.save(outPrefix, Select())
    

def extractPdbChains(pdbFile):
    '''
    Note: removes original PDB file if multiple chains are found.
    ## helper function for "formatPDB_db"
    '''

    from Bio.PDB.PDBParser import PDBParser
    from Bio.PDB.PDBIO import PDBIO
    from Bio.PDB.PDBIO import Select
    import os
    import shutil

    def notHet(residue):
        res = residue.id[0]
        return res != "HETATM"

    ## custom select
    class SelectChain(Select):
        def __init__(self, chain):
            self.chain = chain
        def accept_chain(self, chain):
            # print("[self.chain] " + self)
            # print("[chain.id] " + chain.id)
            if chain == self.chain:
                return 1
            else:
                return 0

    id = os.path.basename(pdbFile).rstrip(".pdb")
    structure = PDBParser().get_structure(id, pdbFile)

    ### Remove all non-amino acid residues
    ### remove chains with only hetatms (small molecules)
    ### remove water molecules
    ### remove nucleic acids
    aaList = ['ALA','CYS','ASP','GLU','PHE','GLY','HIS','ILE','LYS','LEU','MET','ASN','PRO','GLN',
                           'ARG','SER','THR','VAL','TRP','TYR']
    model = structure[0]
    residue_to_remove = []
    chain_to_remove = []
    for chain in model:
        for residue in chain:
            if residue.get_resname() not in aaList:
                # print(residue.get_resname())
            # if residue.id[0] != ' ':
                residue_to_remove.append((chain.id, residue.id))
        if len(chain) == 0:
            chain_to_remove.append(chain.id)
    for residue in residue_to_remove:
        model[residue[0]].detach_child(residue[1])
    for chain in chain_to_remove:
        model.detach_child(chain)

    print(len(list(structure.get_chains())))
    if len(list(structure.get_chains())) < int(1):
        os.remove(pdbFile)
    ## rename with chain ("_A") if only 1 chain
    if len(list(structure.get_chains())) == int(1):
        print("FOUND")
        for chain in structure.get_chains():
            outName = pdbFile.rstrip(".pdb") + "_" + chain.id.upper() + ".pdb"
            print(pdbFile)
            print(outName)
            shutil.copy(src=pdbFile, dst=outName)
    ## if > 1 chain, separate, write, and delete parent pdb
    if len(list(structure.get_chains())) > int(1):
        for chain in structure.get_chains():
            if len(chain) == 0:
                pass
            if len(chain) > 0:
                # for residue in chain:
                # print(chain.get_residues())
                outName = pdbFile.rstrip(".pdb") + "_" + chain.id.upper() + ".pdb"
                # print("[extractPdbChains] write: " + outName)
                io = PDBIO()
                io.set_structure(structure)
                io.save(outName, SelectChain(chain))
        os.remove(pdbFile)

def extractPDB(filename, root, newDir):
    '''
    Note: helper function for "formatPDB_db"
    '''

    import shutil
    import os
    import re
    import gzip

    file = os.path.join(root, filename,)
    ### gunzip and rename to pdb
    if re.search("^.*ent\.gz$", file):
        # print(filename)
        ### strip "pdb" prefix
        name = filename.lstrip('pdb').upper()
        outfile = newDir+"/"+name.rstrip('.ENT.GZ')+".pdb"
        with gzip.open(file, 'rb') as f_in:
            with open(outfile, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    if re.search(".pdb$", file):
        name = filename.rstrip('.pdb').upper()
        outfile = newDir+"/"+name +".pdb"
        # print(outfile)
        shutil.copy(file, outfile)


def formatPDB_db(dbLocation, cores):
    '''
    1. find all pdb or .ent files in dbLocation
    2. if .ent file is gzipped, unzip to .pdb file
    3. create an output subdirectory of dbLocation
            "/FATCATdb_{date}"
    4. extract each chain from pdb files, write to new file, and delete parent pdb
        (if chains exist)
    5. create a log file containing the full path of each pdb file
        (useful for batch processing)
    '''

    ### globs all .ent.gz or .pdb files in dbLocation directory
    import glob
    import os
    from datetime import date
    import multiprocessing as mp

    ### adjust number of cores
    if cores >= int(mp.cpu_count()):
        optCores = int(mp.cpu_count())-1
        # print("Too many cores selected")
        # print("Reducing to " + str(optCores) + " cores")
        cores = optCores
    if cores < int(mp.cpu_count()):
        cores = cores

    ### create output directory for FATCAT db
    newDir = os.path.dirname(dbLocation)+"/FATCATdb_"+str(date.today())
    # print(newDir)
    if os.path.exists(newDir):
        pass
    else:
        os.mkdir(newDir, mode = 0o755)

    ### glob all pdb files (.ent and .pdb files are identical, just different extension)
    for root, dirs, files in os.walk(dbLocation):
        batchDict = {}
        b = 1
        for i in range(0, len(files), cores):
            batchName = "b"+str(b)
            batchDict[batchName] = files[i:i + cores]
            b = b + 1
        # print(batchDict)

        for key, values in batchDict.items():
            # print("[extractPDB]: Processing batch ", key, " of ", len(batchDict))
            procs = []
            # if key == "b1":
            #     print(key, values)
            #     for d in values:
            #         print(d)
            if key:
                for filename in values:
                    # print(inputPDB)
                    # single argument requires a "," after
                    # see: https://stackoverflow.com/questions/1559125/string-arguments-in-python-multiprocessing
                    p = mp.Process(target=extractPDB, args=(filename, root, newDir))
                    procs.append(p)
                    # print(p)
                    p.start()
                for proc in procs:
                    proc.join()

    ### multiprocess extract individual chains from the pdb files
    pdbFiles = glob.glob(newDir+"/*.pdb")
    batchDict = {}
    b = 1
    for i in range(0, len(pdbFiles), cores):
        batchName = "b"+str(b)
        batchDict[batchName] = pdbFiles[i:i + cores]
        b = b + 1
    # print(batchDict)

    for key, values in batchDict.items():
        # print("[extractChains]: Processing batch ", key, " of ", len(batchDict))
        procs = []
        # if key == "b1":
        #     print(key, values)
        #     for d in values:
        #         print(d)
        if key:
            for pdbFile in values:
                # print(inputPDB)
                # single argument requires a "," after
                # see: https://stackoverflow.com/questions/1559125/string-arguments-in-python-multiprocessing
                p = mp.Process(target=extractPdbChains, args=(pdbFile,))
                procs.append(p)
                # print(p)
                p.start()
            for proc in procs:
                proc.join()

    ### generate list of pdb files for FATCATSearch
    pdbFiles = glob.glob(newDir+"/*.pdb")
    # print(len(pdbFiles))
    # for pdbFile in pdbFiles:

    outList = open(newDir+"/FATCAT_list_"+str( date.today() )+".list", "w")
    for file in pdbFiles:
        # print(file)
        # print(os.path.basename(file))
        # outList.write(os.path.basename(file).rstrip(".pdb")+"\n")
        outList.write(file+"\n")
    outList.close()



def jFatCatAlign(queryPDB, targetPDB, javaFullPath, aoFatCatJar,
                 outputDir, alignmentCutoff = 0.05):
    import os
    import subprocess
    if os.path.exists(outputDir):
        pass
    else:
        os.mkdir(outputDir, mode = 0o755)
    proc = subprocess.Popen([javaFullPath, '-jar', aoFatCatJar,
                             queryPDB, targetPDB, str(alignmentCutoff), outputDir],
                            bufsize=-1)
    code=proc.wait()
    # if str(code) == '0':
        # print("[jFatCatAlign]: Success")
    # else:
        # print("[jFatCatAlign]: Failed")


def fatcatMultiProcess(queryPDB, targetPDBList, javaFullPath, aoFatCatJar,
                       outputDir, alignmentCutoff = 0.05, cores = 4):
    import multiprocessing as mp
    import os
    import sys
    import time

    ### create batches list
    if cores >= int(mp.cpu_count()):
        optCores = int(mp.cpu_count())-1
        # print("Too many cores selected")
        # print("Reducing to " + str(optCores) + " cores")
        cores = optCores
    if cores < int(mp.cpu_count()):
        cores = cores     
    file = open(targetPDBList, 'r')
    lines = file.readlines()
    lines2 = []
    for line in lines:
        line = line.rstrip("\n")
        lines2.append(line)
    batchDict = {}
    b = 1
    for i in range(0, len(lines2), cores):
        batchName = "b"+str(b)
        batchDict[batchName] = lines2[i:i + cores]
        b = b + 1
    # print(batchDict)
    file.close()
    
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