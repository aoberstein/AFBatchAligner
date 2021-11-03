#!/usr/bin/python3
import os
import re
import shutil

# target files to be renamed/formatted
#AF_output_root = "/home/adam/nvme/alphafold_output_sync"
AF_output_root = "/home/adam/archive/af_alignments/HHV6A_U1102"

# fatcat input directory to hold query files, which will be filtered by b-value next
dbDir = "/home/adam/archive/af_alignments/HHV6A_U1102/fatcat_queries"

# check that dbDir exists and create if absent
if os.path.exists(dbDir):
    pass
else:
    os.mkdir(dbDir, mode = 0o755)


for root, dirs, files in os.walk(AF_output_root):
    # for dir in dirs:
      # print(dir)
    for filename in files:
        file = os.path.join(root, filename)
        # print(os.path.basename(root))
        # print(file)
        genePrefix = os.path.basename(root)
        if re.search("^.*ranked_0.pdb$", file):
          # print(root)
          # print(file)
          # print(genePrefix)
          print(dbDir+"/"+genePrefix+".pdb")
          shutil.copy(file, dbDir+"/"+genePrefix+".pdb")
