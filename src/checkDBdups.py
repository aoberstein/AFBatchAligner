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
    outfile = open(PdbListFile + ".temp", "w")
    for line in dedupList:
        outfile.write(line)
    outfile.close()

# file = "/home/adam/archive/db/pdb/2021-10-26/pdb_clusters/bc-40.list"
# # checkDups(file)
# # removeDups(file)
# checkDups("/home/adam/archive/db/pdb/2021-10-26/pdb_clusters/bc-40.list.temp")