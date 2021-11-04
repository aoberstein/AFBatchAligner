#!/usr/bin/python3

from fatcat_functions import filterPDB
import glob
import re

def main():
    
    ''' FILTER INPUT FILE BY PREDICTION CONFIDENCE (b-factor) '''
    files = glob.glob("/home/adam/archive/intellij-workspace/test_area/db/FATCATdb_2021-10-22/*.pdb")
    cutoff = 30.00

    ## filter files based on b-factor (alphafold places confidence in b-factor of pdb file)
    for file in files:
        if re.match(".*_bFILT.*", file):
            continue
        else:    
            print(file)
            filterPDB(file, cutoff)


if __name__ == '__main__':
    main()
    
    


