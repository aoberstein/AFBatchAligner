#!/usr/bin/python3
import os
import re
import shutil

AF_output_root = "/home/adam/nvme/alphafold_output_sync"
inputDir = "/mnt/nvme_scratch/2021-10-04_fatcat_HCMV_self_to_self_run1/input"
dbDir = "/mnt/nvme_scratch/2021-10-04_fatcat_HCMV_self_to_self_run1/db"

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
          print(inputDir+"/"+genePrefix+".pdb")
          shutil.copy(file, inputDir+"/"+genePrefix+".pdb")
          shutil.copy(file, dbDir+"/"+genePrefix+".pdb")
