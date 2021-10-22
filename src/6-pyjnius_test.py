#!/usr/bin/python3

from fatcat_functions import *
import glob
from pathlib import Path
import jpype

# jpype.addClassPath("/home/adam/archive/eclipse-workspace/java_export/biojava.jar")
jpype.addClassPath("/home/adam/archive/eclipse-workspace/java_export/com.adam.fatcat.copy-0.0.1-SNAPSHOT.jar")
jpype.startJVM()
#jpype.JClass("/home/adam/archive/eclipse-workspace/java_export/com.adam.aofatcat/com.adam.aofatcat.align.class")
print(jpype.java.lang.System.getProperty("java.class.path"))
from aofatcat import align


# import jpype.imports
# from jpype.types import *
# from jpype import javax
# # jpype.startJVM(classpath=['/usr/lib/jvm/java-1.11.0-openjdk-amd6/lib', 
# jpype.startJVM(classpath=['/home/adam/archive/eclipse-workspace/com.adam.aofatcat.jar'])
# # jpype.startJVM()
# from java.lang import System
# from com.adam.aofatcat import 
def main():

    pdbRootFolderString = "/home/adam/archive/eclipse-workspace/com.adam.fatcat.align/files/"
    pdb1 = pdbRootFolderString + "3cna.pdb"
    pdb2 = pdbRootFolderString + "2pel.pdb"
    flexible = "true"
    result = align.alignLocalPDBs(pdb1, pdb2, bool(flexible))
    print(result)
    # lines = result.readlines()
    # for line in lines:
    #     print(line)
    jpype.stopJVM()

    
if __name__ == '__main__':
    main()
    
    


