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



