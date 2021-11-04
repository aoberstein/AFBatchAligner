#!/usr/bin/python3

from formatPdbClusters import *

def main():

    ### check cluster file for dups
    clusterFile = "/mnt/rip1/archive/db/pdb/2021-10-26/pdb_clusters/bc-40_filt80.list"
    clusterFile2 = "/mnt/rip1/archive/db/pdb/2021-10-26/pdb_clusters/bc-40_filt80_deDup.list"
    checkDups(PdbListFile=clusterFile)
    removeDups(PdbListFile=clusterFile)
    checkDups(PdbListFile=clusterFile2)

if __name__ == '__main__':
    main()