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
    

def formatPDB_db(dbLocation):
    ### globs all .ent.gz or .pdb files in dbLocation directory
    import glob
    import os
    from datetime import date
    import re
    import shutil
    import gzip
    ### create output directory for FATCAT db
    newDir = os.path.dirname(dbLocation)+"/FATCATdb_"+str(date.today())
    # print(newDir)
    if os.path.exists(newDir):
        pass
    else:
        os.mkdir(newDir, mode = 0o755)
    ### glob all pdb files (.ent and .pdb files are identical,
    # just different extension)
    for root, dirs, files in os.walk(dbLocation):
        for filename in files:
            file = os.path.join(root, filename)
            print(file)
            ### gunzip and rename to pdb
            if re.search("^.*ent\.gz$", file):
                # print(filename)
                ### strip "pdb" prefix
                outfile = newDir+"/"+filename.lstrip('pdb').rstrip('.ent.gz')+".pdb"
                with gzip.open(file, 'rb') as f_in:
                    with open(outfile, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            if re.search("^.*.pdb", file):
                print(newDir+"/"+os.path.basename(file))
                shutil.copy(file, newDir+"/"+os.path.basename(file))
    ### generate list of pdb files for FATCATSearch
    pdbFiles = glob.glob(newDir+"/*.pdb")
    print(len(pdbFiles))
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
    if str(code) == '0':
        print("[jFatCatAlign]: Success")
    else:
        print("[jFatCatAlign]: Failed")


def fatcatMultiProcess(queryPDB, targetPDBList, javaFullPath, aoFatCatJar,
                       outputDir, alignmentCutoff = 0.05, cores = 4):
    import multiprocessing as mp
    import os
    ### create batches list
    if cores >= int(mp.cpu_count()):
        optCores = int(mp.cpu_count())-1
        print("Too many cores selected")
        print("Reducing to " + str(optCores) + " cores")
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
    
    ### multiprocess with fatcat
    for key, values in batchDict.items():
        procs = []
        # if key == "b1":
        #     print(key, values)
        if key:    
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

