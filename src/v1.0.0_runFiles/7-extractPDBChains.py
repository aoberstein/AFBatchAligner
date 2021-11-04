#!/usr/bin/python3

from fatcat_functions import extractPdbChains
from fatcat_functions import formatPDB_db

### test single file chain extractor
# pdbFile = "/home/adam/archive/intellij-workspace/test_area/extractChains_test_folder/2pel.pdb"
# extractPdbChains(pdbFile)

### format database of pdbs including chain extraction
dbLocation="/home/adam/archive/intellij-workspace/test_area/extractChains_test_folder"
formatPDB_db(dbLocation=dbLocation)
