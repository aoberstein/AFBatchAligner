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