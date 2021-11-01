#!/usr/bin/python3

from lengthFilterClusters import lengthFilter

## format pdb database (exclude all non-AA residues and chains)
clusterList = "/home/adam/archive/db/pdb/2021-10-26/pdb_clusters/bc-40.list"
lengthToPdbTSV = "/home/adam/archive/db/pdb/2021-10-26/FATCATdb_2021-11-01/pdbLengths.tsv"
lengthFilter( clusterList, lengthToPdbTSV, 60)