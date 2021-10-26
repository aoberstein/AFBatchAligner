#!/usr/bin/python3

from fatcat_functions import formatPDB_db

## format pdb database (exclude all non-AA residues and chains)
dbRoot = "/home/adam/archive/db/pdb/2021-10-26/pdb"
formatPDB_db(dbLocation=dbRoot, cores=32)
