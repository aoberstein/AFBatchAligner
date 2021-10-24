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
            "Init. length\tOpt. Equiv.\tInit. rmsd\tOpt. rmsd\t" +\
            "Chain rmsd\tp-value\tscore\tTotAlign Length\tGap Length\t" +\
            "%Gaps of align\tAFP number\tIdent. (%)\tSimilar (%)\t" +\
            "Alignment txt File\tAlignment PDB File"
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
       pdbFile = Dir + "/" + pdb1 + "_" + pdb2 + "_alignment.pdb"
       txtFile = Dir + "/" + pdb1 + "_" + pdb2 + "_FatCat.txt"
       # print(stats)
       # print(pdbFile)
       # print(txtFile)
       outLines.append("%s\t%s\t%s" % (stats, txtFile, pdbFile))

   print(outLines)
   ## write formatted xls file
   writeDir = Dir
   print(writeDir)
   workbook = xlsxwriter.Workbook(writeDir + "0_" + queryPrefix + "_summary.xlsx")
   center_format = workbook.add_format()
   center_format.set_align('center')
   # left_format = workbook.add_format()
   # left_format.set.align('left')
   percent_format = workbook.add_format({'num_format': '0.0'})
   percent_format.set_align('center')
   rmsd_format = workbook.add_format({'num_format': '0.00'})
   rmsd_format.set_align('center')
   sci_format = workbook.add_format({'num_format': '0.00E+00'})
   sci_format.set_align('center')
   file_link_format = workbook.add_format({'bold': False, 'underline':True, 'font_color': 'blue'})
   header_format1 = workbook.add_format({'bold': True, 'text_wrap': True})
   header_format1.set_align('center')
   header_format2 = workbook.add_format({'bold': True, 'text_wrap': True})
   header_format2.set_align('left')

   ## global formatting for workbook
   worksheet = workbook.add_worksheet()
   worksheet.set_row(0, 40)
   worksheet.set_column(0, 1, 23)
   worksheet.set_column(20, 21, 25)
   # worksheet.set_colum(2, 19, None, center_format)

   for row,line in enumerate(outLines):
       print(row)
       data = line.split('\t')
       if int(row) == 0:
           worksheet.write(row, 0, data[0], header_format2) #Query
           worksheet.write(row, 1, data[1], header_format2) #Target
           worksheet.write(row, 2, data[2], header_format1) #Query Length
           worksheet.write(row, 3, data[3], header_format1) #Target Length
           worksheet.write(row, 4, data[4], header_format1) #Twists
           worksheet.write(row, 5, data[5], header_format1) #Percent Query Aligned
           worksheet.write(row, 6, data[6], header_format1) #Percent Target Aligned
           worksheet.write(row, 7, data[7], header_format1) #Init. length
           worksheet.write(row, 8, data[8], header_format1) #Opt. Equivalent
           worksheet.write(row, 9, data[9], header_format1) #Init. rmsd
           worksheet.write(row, 10, data[10], header_format1) #Opt. rmsd
           worksheet.write(row, 11, data[11], header_format1) #Chain rmsd
           worksheet.write(row, 12, data[12], header_format1) #p-value
           worksheet.write(row, 13, data[13], header_format1) #score
           worksheet.write(row, 14, data[14], header_format1) #TotAlign Length
           worksheet.write(row, 15, data[15], header_format1) #Gap Length
           worksheet.write(row, 16, data[16], header_format1) #%Gaps of align
           worksheet.write(row, 17, data[17], header_format1) #AFP number
           worksheet.write(row, 18, data[18], header_format1) #Identity(%)
           worksheet.write(row, 19, data[19], header_format1) #Similarity(%)
           worksheet.write(row, 20, data[20], header_format2) # Alignment txt file
           worksheet.write(row, 21, data[21], header_format2) #Alignment pdb File
       else:
           worksheet.write(row, 0, data[0]) #Query
           worksheet.write(row, 1, data[1]) #Target
           worksheet.write(row, 2, data[2], center_format) #Query Length
           worksheet.write(row, 3, data[3], center_format) #Target Length
           worksheet.write(row, 4, data[4], center_format) #Twists
           worksheet._write(row, 5, float(data[5]), percent_format) #Percent Query Aligned
           worksheet._write(row, 6, float(data[6]), percent_format) #Percent Target Aligned
           worksheet.write(row, 7, data[7], center_format) #Init. length
           worksheet.write(row, 8, data[8], center_format) #Opt. Equivalent
           worksheet.write(row, 9, float(data[9]), rmsd_format) #Init. rmsd
           worksheet.write(row, 10, float(data[10]), rmsd_format) #Opt. rmsd
           worksheet.write(row, 11, float(data[11]), rmsd_format) #Chain rmsd
           worksheet.write(row, 12, float(data[12]), sci_format) #p-value
           worksheet.write(row, 13, float(data[13]), percent_format) #score
           worksheet.write(row, 14, data[14], center_format) #TotAlign Length
           worksheet.write(row, 15, data[15], center_format) #Gap Length
           worksheet.write(row, 16, float(data[16]), percent_format) #%Gaps of align
           worksheet.write(row, 17, data[17], center_format) #AFP number
           worksheet.write(row, 18, float(data[18]), percent_format) #Identity(%)
           worksheet.write(row, 19, float(data[19]), percent_format) #Similarity(%)
           worksheet.write_url(row, 20, data[20], file_link_format) # Alignment txt file
           worksheet.write_url(row, 21, data[21], file_link_format) #Alignment pdb File
   workbook.close()















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
