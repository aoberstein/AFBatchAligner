#!/usr/bin/python3

# from fatcat_functions import formatPDB_db
from formatPdbClusters import extractPdbClusters


## format clusters
clusterFile = "/home/adam/archive/db/pdb/2021-10-26/pdb_clusters/bc-40.out"
dbDir = "/home/adam/archive/db/pdb/2021-10-26/FATCATdb_2021-11-01"
extractPdbClusters(clusterFile, dbDir)


# ## format pdb database (exclude all non-AA residues and chains)
# dbRoot = "/home/adam/archive/db/pdb/2021-10-26/pdb"
# formatPDB_db(dbLocation=dbRoot, cores=28)

