#!/usr/bin/python3

def extractPdbClusters(clusterFile, dbDir):
    import os

    outPath = os.path.dirname(clusterFile)
    print("[outpath]: " + outPath)
    outName = clusterFile.rstrip(".out") + ".list"
    fout = open(outName, "w")
    print(outName)

    lines = open(clusterFile, "r").readlines()
    for line in lines:
        line = line.strip()
        pdb = line.split(" ")[0]
        id = pdb.split("_")[0]
        chain = pdb.split("_")[1].rstrip(".pdb").upper()
        #id = id.lower()
        fout.write(dbDir + "/" + id + "_" + chain + ".pdb\n")
    fout.close()

def lengthFilter(clusterList, lengthToPdbTSV, maxLength):
    '''lengthToPdbTSV has have identical root path on each entry'''
    import os

    table = open(lengthToPdbTSV, "r").readlines()

    root = os.path.dirname(table[0])
    print(root)
    # print(type(table))
    ### create dict of key = pdbPrefix; value = length
    lengthDict = {}
    for entry in table:
        entry = entry.strip()
        pdb = os.path.basename(entry.split('\t')[0])
        length = entry.split('\t')[1]
        if int(length) >= maxLength:
            lengthDict[pdb] = length

    # print(lengthDict)
    clusters = open(clusterList, "r").readlines()
    clusterPath = os.path.dirname(clusterList)
    clusterPrefix = os.path.basename(clusterList).strip(".list")
    print(clusterPath + "/" + clusterPrefix + "_filt" + str(maxLength) + ".list")
    outFile = open(clusterPath + "/" + clusterPrefix + "_filt" + str(maxLength) + ".list", "w")
    for pdbPath in clusters:
        pdb = os.path.basename(pdbPath).strip()
        # print(pdb)
        if pdb in lengthDict.keys():
            # print(lengthDict[pdb])
            outFile.write(root + "/" + pdb + "\n")
    outFile.close()

def checkDups(PdbListFile):
    data = open(PdbListFile, "r")
    lines = data.readlines()
    dups = [i for i, x in enumerate(lines) if lines.count(x) > 1]
    print(dups)

def removeDups(PdbListFile):
    data = open(PdbListFile, "r")
    lines = data.readlines()
    dedupList = list(dict.fromkeys(lines))
    data.close()
    newName = PdbListFile.rstrip(".list") + "_deDup.list"
    outfile = open(newName, "w")
    for line in dedupList:
        outfile.write(line)
    outfile.close()