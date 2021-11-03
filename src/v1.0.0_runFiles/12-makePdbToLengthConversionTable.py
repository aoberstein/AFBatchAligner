#!/usr/bin/python3

from pdbTools import exportPdbToLengths


def main():

    # ## format clusters (append dbDir folder to first pdb in each cluster)
    clusterFile = "/home/adam/archive/db/pdb/2021-10-26/pdb_clusters/bc-40.out"
    dbDir = "/home/adam/archive/db/pdb/2021-10-26/FATCATdb_2021-10-28"
    extractPdbClusters(clusterFile, dbDir)


    # ## format pdb database (exclude all non-AA residues and chains)
    # dbRoot = "/home/adam/archive/db/pdb/2021-10-26/FATCATdb_2021-10-28"
    dbRoot = "/home/adam/archive/db/pdb/2021-10-26/test2"
    # dbRoot = checkFolderBackslash(dbRoot)
    # print(dbRoot)
    # formatPDB_db(dbLocation=dbRoot, cores=28)
    exportPdbToLengths(dbFolder=dbRoot, cores = 32)


if __name__ == '__main__':
    main()