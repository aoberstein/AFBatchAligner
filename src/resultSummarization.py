def FCtoXls(Dir):
   import glob
   import os
   import os.path
   import shutil
   import xlsxwriter
   import re

   ## Get directory structure
   # Dir should be the directory named after the alignment queryPDB
   # expect each directory to have an "fcWriteTemp" subfolder
   # check for trailing slash on Dir and add if missing
   if Dir[-1] == "/":
       pass
   else:
       Dir = Dir + "/"

   queryPrefix = os.path.basename(Dir.rstrip("/"))
   print(queryPrefix)
   subDir = Dir + "fcWriteTemp/"
   files = glob.glob(subDir + "*_fcLine.tab")
   header = "Query\tTarget\tQuery Length\tTarget Length\t" +\
            "Twists\tPercent Query Aligned\tPercent Target Aligned\t" +\
            "Init. length\tOpt. Equivalent\tInit. rmsd\tOpt. rmsd\t" +\
            "Chain rmsd\tp-value\tscore\tTotAlign Length\tGap Length\t" +\
            "%Gaps of align\tAFP number\tIdentity(%)\tSimilarity(%)\t" +\
            "Alignment PDB File\tAlignment txt File"
   print(header)

   outLines = []
   outLines.append(header)
   for file in files:
       handle = open(file, "r")
       stats = handle.readlines()[1]
       stats = stats.strip()
       stats = re.sub("\s+", "\t", stats)
       pdb1 = stats.split('\t')[0]
       pdb2 = stats.split('\t')[1]
       pdbFile = Dir + "/" + pdb1 + "/" + pdb1 + "_" + pdb2 + "_alignment.pdb"
       txtFile = Dir + "/" + pdb1 + "/" + pdb1 + "_" + pdb2 + "_FatCat.txt"
       # print(stats)
       # print(pdbFile)
       # print(txtFile)
       outLines.append("%s\t%s\t%s" % (stats, pdbFile, txtFile))

   print(outLines)
   ## write formatted xls file
   writeDir = Dir
   print(writeDir)
   workbook = xlsxwriter.Workbook(writeDir + "0_" + queryPrefix + "_summary.xlsx")
   worksheet = workbook.add_worksheet()
   for row,line in enumerate(outLines):
       data = line.split('\t')
       worksheet.write(row, 0, data[0]) #Query
       worksheet.write(row, 1, data[1]) #Target
       worksheet.write(row, 2, data[2]) #Query Length
       worksheet.write(row, 3, data[3]) #Target Length

       worksheet.write(row, 4, data[4]) #Twists
       worksheet.write(row, 5, data[5]) #Percent Query Aligned
       worksheet.write(row, 6, data[6]) #Percent Target Aligned
       worksheet.write(row, 7, data[7]) #Init. length

       worksheet.write(row, 8, data[8]) #Opt. Equivalent
       worksheet.write(row, 9, data[9]) #Init. rmsd
       worksheet.write(row, 10, data[10]) #Opt. rmsd
       worksheet.write(row, 11, data[11]) #Chain rmsd

       worksheet.write(row, 12, data[12]) #p-value
       worksheet.write(row, 13, data[13]) #score
       worksheet.write(row, 14, data[14]) #TotAlign Length
       worksheet.write(row, 15, data[15]) #Gap Length

       worksheet.write(row, 16, data[16]) #%Gaps of align
       worksheet.write(row, 17, data[17]) #AFP number\tIdentity(%)
       worksheet.write(row, 18, data[18]) #Similarity(%)
       worksheet.write(row, 19, data[19]) #Alignment PDB File

       worksheet.write(row, 20, data[20]) #Alignment txt File
   workbook.close()

       # header = "Query\t" \
       #          "Target\t" \
       #          "Query Length" \
       #          "\tTarget Length" \

       #          "Twists\t" \
       #          "Percent Query Aligned" \
       #          "\tPercent Target Aligned" \
       #          "\t"Init. length

       #            \tOpt. Equivalent
       #            \tInit. rmsd
       #            \tOpt. rmsd\t" + \
       #          "Chain rmsd\

       #          p-value
       #          \tscore
       #          \tTotAlign Length
       #          \tGap Length\t" + \

       #          "%Gaps of align
       #          \tAFP number\tIdentity(%)
       #          \tSimilarity(%)\t" + \
       #          "Alignment PDB File

       #          \tAlignment txt File"













# def catFatcatTempFilesBatch(outputDir):
#     import multiprocessing as mp
#     import os
#
#     ### create batches list
#     if cores >= int(mp.cpu_count()):
#         optCores = int(mp.cpu_count())-1
#         print("Too many cores selected")
#         print("Reducing to " + str(optCores) + " cores")
#         cores = optCores
#     if cores < int(mp.cpu_count()):
#         cores = cores
#     file = open(targetPDBList, 'r')
#     lines = file.readlines()
#     lines2 = []
#     for line in lines:
#         line = line.rstrip("\n")
#         lines2.append(line)
#     batchDict = {}
#     b = 1
#     for i in range(0, len(lines2), cores):
#         batchName = "b"+str(b)
#         batchDict[batchName] = lines2[i:i + cores]
#         b = b + 1
#     # print(batchDict)
#     file.close()
#
#     ### create output subdirectories
#     # query = os.basename(queryPDB)
#     queryPrefix = os.path.basename(queryPDB).rstrip(".pdb")
#     subDir = outputDir+"/"+queryPrefix
#     if os.path.exists(subDir):
#         pass
#     else:
#         os.mkdir(subDir, mode = 0o755)
#
#     ### multiprocess with fatcat
#     for key, values in batchDict.items():
#         procs = []
#         # if key == "b1":
#         #     print(key, values)
#         if key:
#             for targetPDB in values:
#                 targetPDB = targetPDB.strip()
#                 # print(targetPDB)
#                 p = mp.Process(target=jFatCatAlign,
#                                args=(queryPDB, targetPDB, javaFullPath, aoFatCatJar,
#                                      subDir, alignmentCutoff))
#                 procs.append(p)
#                 # print(procs)
#                 p.start()
#             for proc in procs:
#                 proc.join()
#
