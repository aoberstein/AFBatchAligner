#!/usr/bin/python3

from fatcat_functions3 import formatPDB_db

## format pdb database (exclude all non-AA residues and chains)
dbRoot = "/home/adam/projects/2021-11-01_U94_analysis/db"
formatPDB_db(dbLocation=dbRoot, cores=32)