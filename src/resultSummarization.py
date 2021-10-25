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
   right_format = workbook.add_format()
   right_format.set_align('right')
   percent_format = workbook.add_format({'num_format': '0.0'})
   percent_format.set_align('center')
   rmsd_format = workbook.add_format({'num_format': '0.00'})
   rmsd_format.set_align('center')
   sci_format = workbook.add_format({'num_format': '0.00E+00'})
   sci_format.set_align('center')
   file_link_format = workbook.add_format({'bold': False, 'underline':True, 'font_color': 'blue'})
   file_link_format.set_align('right')

   header_format1 = workbook.add_format({'bold': True, 'text_wrap': True})
   header_format1.set_align('center')
   header_format2 = workbook.add_format({'bold': True, 'text_wrap': True})
   header_format2.set_align('right')

   ## global formatting for workbook
   worksheet = workbook.add_worksheet()
   worksheet.set_row(0, 40)
   worksheet.set_column(0, 1, 20)
   worksheet.set_column(16, 17, 25)
   # worksheet.set_column(21, 21, 25)
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
           # worksheet.write(row, 7, data[7], header_format1) #Init. length
           worksheet.write(row, 7, data[8], header_format1) #Opt. Equivalent
           # worksheet.write(row, 9, data[9], header_format1) #Init. rmsd
           worksheet.write(row, 8, data[10], header_format1) #Opt. rmsd
           worksheet.write(row, 9, data[11], header_format1) #Chain rmsd
           worksheet.write(row, 10, data[12], header_format1) #p-value
           worksheet.write(row, 11, data[13], header_format1) #score
           worksheet.write(row, 12, data[14], header_format1) #TotAlign Length
           # worksheet.write(row, 15, data[15], header_format1) #Gap Length
           worksheet.write(row, 13, data[16], header_format1) #%Gaps of align
           # worksheet.write(row, 17, data[17], header_format1) #AFP number
           worksheet.write(row, 14, data[18], header_format1) #Identity(%)
           worksheet.write(row, 15, data[19], header_format1) #Similarity(%)
           worksheet.write(row, 16, data[20], header_format2) # Alignment txt file
           worksheet.write(row, 17, data[21], header_format2) #Alignment pdb File
       else:
           worksheet.write(row, 0, data[0], right_format) #Query
           worksheet.write(row, 1, data[1], right_format) #Target
           worksheet.write(row, 2, data[2], center_format) #Query Length
           worksheet.write(row, 3, data[3], center_format) #Target Length
           worksheet.write(row, 4, data[4], center_format) #Twists
           worksheet._write(row, 5, float(data[5]), percent_format) #Percent Query Aligned
           worksheet._write(row, 6, float(data[6]), percent_format) #Percent Target Aligned
           # worksheet.write(row, 7, data[7], center_format) #Init. length
           worksheet.write(row, 7, data[8], center_format) #Opt. Equivalent
           # worksheet.write(row, 9, float(data[9]), rmsd_format) #Init. rmsd
           worksheet.write(row, 8, float(data[10]), rmsd_format) #Opt. rmsd
           worksheet.write(row, 9, float(data[11]), rmsd_format) #Chain rmsd
           worksheet.write(row, 10, float(data[12]), sci_format) #p-value
           worksheet.write(row, 11, float(data[13]), percent_format) #score
           worksheet.write(row, 12, data[14], center_format) #TotAlign Length
           # worksheet.write(row, 15, data[15], center_format) #Gap Length
           worksheet.write(row, 13, float(data[16]), percent_format) #%Gaps of align
           # worksheet.write(row, 17, data[17], center_format) #AFP number
           worksheet.write(row, 14, float(data[18]), percent_format) #Identity(%)
           worksheet.write(row, 15, float(data[19]), percent_format) #Similarity(%)
           worksheet.write_url(row, 16, data[20], file_link_format, string=os.path.basename(data[20])) # Alignment txt file
           worksheet.write_url(row, 17, data[21], file_link_format, string=os.path.basename(data[21])) #Alignment pdb File
   workbook.close()


def pandasToXls(Dir):
    import glob
    import os
    import os.path
    import shutil
    import xlsxwriter
    import re
    import pandas

    ## Get directory structure
    # Dir should be the directory named after the alignment queryPDB
    # expect each directory to have an "fcWriteTemp" subfolder
    # check for trailing slash on Dir and add if missing
    if Dir[-1] == "/":
        pass
    else:
        Dir = Dir + "/"

    queryPrefix = os.path.basename(Dir.rstrip("/"))
    # print(queryPrefix)
    subDir = Dir + "fcWriteTemp/"
    files = glob.glob(subDir + "*_fcLine.tab")
    header = ["Query", "Target", "Query Length", "Target Length",
             "Twists", "Percent Query Aligned", "Percent Target Aligned",
             "Init. length", "Opt. Equiv.", "Init. rmsd", "Opt. rmsd",
             "Chain rmsd", "p-value", "score", "TotAlign Length", "Gap Length",
             "%Gaps of align", "AFP number", "Ident. (%)", "Similar (%)",
             "Alignment txt File", "Alignment PDB File"]

    ## coerce lists of lists to pd.DataFrame (allows sorting)
    outLines = []
    outLines.append(header)
    for file in files:
        handle = open(file, "r")
        stats = handle.readlines()[1]
        stats = stats.strip()
        stats = re.sub("\s+", "\t", stats)
        statList = stats.split('\t')
        pdb1 = stats.split('\t')[0]
        pdb2 = stats.split('\t')[1]
        pdbFile = Dir + "/" + pdb1 + "_" + pdb2 + "_alignment.pdb"
        txtFile = Dir + "/" + pdb1 + "_" + pdb2 + "_FatCat.txt"
        statList.append(txtFile)
        statList.append(pdbFile)

        # print(stats)
        # print(pdbFile)
        # print(txtFile)
        outLines.append(statList)
    # print(outLines)
    df = pandas.DataFrame(columns = outLines[0], data = outLines[1:])
    # df = pandas.DataFrame(outLines)
    # print(df.columns)
    # print(df.index)

    ## sort df
    df["score"] = pandas.to_numeric(df["score"])
    df.sort_values(by="score", ascending=False, inplace=True)
    print(df['score'])

    ## remove some columns
    df = df.drop(columns=['Init. length', 'Init. rmsd', 'Gap Length', 'AFP number'])

    ## coerce back to list of list (since I already have excel formatting for list)
    header = df.columns.tolist()
    outLines = df.values.tolist()
    print(header)
    print(outLines)
    
    ## write formatted xls file
    writeDir = Dir
    print(writeDir)
    workbook = xlsxwriter.Workbook(writeDir + "0_" + queryPrefix + "_summary.xlsx")
    center_format = workbook.add_format()
    center_format.set_align('center')
    right_format = workbook.add_format()
    right_format.set_align('right')
    percent_format = workbook.add_format({'num_format': '0.0'})
    percent_format.set_align('center')
    rmsd_format = workbook.add_format({'num_format': '0.00'})
    rmsd_format.set_align('center')
    sci_format = workbook.add_format({'num_format': '0.00E+00'})
    sci_format.set_align('center')
    file_link_format = workbook.add_format({'bold': False, 'underline':True, 'font_color': 'blue'})
    file_link_format.set_align('right')
    
    header_format1 = workbook.add_format({'bold': True, 'text_wrap': True})
    header_format1.set_align('center')
    header_format2 = workbook.add_format({'bold': True, 'text_wrap': True})
    header_format2.set_align('right')
    
    ## global formatting for workbook
    worksheet = workbook.add_worksheet()
    worksheet.set_row(0, 40)
    worksheet.set_column(0, 1, 20)
    worksheet.set_column(16, 17, 25)
    # worksheet.set_column(21, 21, 25)
    # worksheet.set_colum(2, 19, None, center_format)
    
    ## write header with formatting
    worksheet.write(0, 0, header[0], header_format2) #Query
    worksheet.write(0, 1, header[1], header_format2) #Target
    worksheet.write(0, 2, header[2], header_format1) #Query Length
    worksheet.write(0, 3, header[3], header_format1) #Target Length
    worksheet.write(0, 4, header[4], header_format1) #Twists
    worksheet.write(0, 5, header[5], header_format1) #Percent Query Aligned
    worksheet.write(0, 6, header[6], header_format1) #Percent Target Aligned
    # worksheet.write(0, 7, header[7], header_format1) #Init. length
    worksheet.write(0, 7, header[7], header_format1) #Opt. Equivalent
    # worksheet.write(0, 9, header[9], header_format1) #Init. rmsd
    worksheet.write(0, 8, header[8], header_format1) #Opt. rmsd
    worksheet.write(0, 9, header[9], header_format1) #Chain rmsd
    worksheet.write(0, 10, header[10], header_format1) #p-value
    worksheet.write(0, 11, header[11], header_format1) #score
    worksheet.write(0, 12, header[12], header_format1) #TotAlign Length
    # worksheet.write(0, 15, header[15], header_format1) #Gap Length
    worksheet.write(0, 13, header[13], header_format1) #%Gaps of align
    # worksheet.write(0, 17, header[17], header_format1) #AFP number
    worksheet.write(0, 14, header[14], header_format1) #Identity(%)
    worksheet.write(0, 15, header[15], header_format1) #Similarity(%)
    worksheet.write(0, 16, header[16], header_format2) # Alignment txt file
    worksheet.write(0, 17, header[17], header_format2) #Alignment pdb File

    ## write data with formatting
    for index,list in enumerate(outLines):
        row = index + 1 ##(acount for lack of header in this list)
        data = list
        worksheet.write(row, 0, data[0], right_format) #Query
        worksheet.write(row, 1, data[1], right_format) #Target
        worksheet.write(row, 2, data[2], center_format) #Query Length
        worksheet.write(row, 3, data[3], center_format) #Target Length
        worksheet.write(row, 4, data[4], center_format) #Twists
        worksheet._write(row, 5, float(data[5]), percent_format) #Percent Query Aligned
        worksheet._write(row, 6, float(data[6]), percent_format) #Percent Target Aligned
        # worksheet.write(row, 7, data[7], center_format) #Init. length
        worksheet.write(row, 7, data[7], center_format) #Opt. Equivalent
        # worksheet.write(row, 9, float(data[9]), rmsd_format) #Init. rmsd
        worksheet.write(row, 8, float(data[8]), rmsd_format) #Opt. rmsd
        worksheet.write(row, 9, float(data[9]), rmsd_format) #Chain rmsd
        worksheet.write(row, 10, float(data[10]), sci_format) #p-value
        worksheet.write(row, 11, float(data[11]), percent_format) #score
        worksheet.write(row, 12, data[12], center_format) #TotAlign Length
        # worksheet.write(row, 15, data[15], center_format) #Gap Length
        worksheet.write(row, 13, float(data[13]), percent_format) #%Gaps of align
        # worksheet.write(row, 17, data[17], center_format) #AFP number
        worksheet.write(row, 14, float(data[14]), percent_format) #Identity(%)
        worksheet.write(row, 15, float(data[15]), percent_format) #Similarity(%)
        worksheet.write_url(row, 16, data[16], file_link_format, string=os.path.basename(data[16])) # Alignment txt file
        worksheet.write_url(row, 17, data[17], file_link_format, string=os.path.basename(data[17])) #Alignment pdb File

    workbook.close()
    
    
    
    
    




#     writeDir = Dir
#     # workbook = xlsxwriter.Workbook(writeDir + "0_" + queryPrefix + "_summary.xlsx")
#     writer = pandas.ExcelWriter(writeDir + "0_" + queryPrefix + "_summary.xlsx", engine='xlsxwriter')
#     df.to_excel(writer, sheet_name='Sheet1', index=False)
#     workbook  = writer.book
#     worksheet = writer.sheets['Sheet1']
#     # writer.save()
# 
#     # workbook = xlsxwriter.Workbook(writeDir + "0_" + queryPrefix + "_summary.xlsx")
#     center_format = workbook.add_format()
#     center_format.set_align('center')
#     right_format = workbook.add_format()
#     right_format.set_align('right')
#     percent_format = workbook.add_format({'num_format': '0.0'})
#     percent_format.set_align('center')
#     rmsd_format = workbook.add_format({'num_format': '0.00'})
#     rmsd_format.set_align('center')
#     sci_format = workbook.add_format({'num_format': '0.00E+00'})
#     sci_format.set_align('center')
#     file_link_format = workbook.add_format({'bold': False, 'underline':True, 'font_color': 'blue'})
#     file_link_format.set_align('right')
# 
#     header_format1 = workbook.add_format({'bold': True, 'text_wrap': True})
#     header_format1.set_align('center')
#     header_format2 = workbook.add_format({'bold': True, 'text_wrap': True})
#     header_format2.set_align('right')
# 
#     ## global formatting for workbook
#     # worksheet = workbook.add_worksheet()
#     worksheet.set_row(0, 40)
#     worksheet.set_column(0, 1, 20)
#     worksheet.set_column(16, 17, 25)
#     worksheet.set_column('A:B', None, right_format ) # A:B right formatted text
#     worksheet.set_column('C:Z', None, center_format ) # c-E, H, M, int/center
#     worksheet.set_column('C:Z', None, center_format ) # I,J, rmsd (0.00)/center
#     worksheet.set_column('C:Z', None, center_format ) # F,G, O, P percent/center (0.0)
#     worksheet.set_column('C:Z', None, center_format ) # K, sci/center (o.00E00)
#     worksheet.set_column('C:Z', None, center_format ) # Q, R url/left
#     # worksheet.set_column(21, 21, 25)
#     # worksheet.set_colum(2, 19, None, center_format)
#     writer.save()
# 
#     # worksheet.write(row, 0, data[0], header_format2) #Query
#     # worksheet.write(row, 1, data[1], header_format2) #Target
#     # worksheet.write(row, 2, data[2], header_format1) #Query Length
#     # worksheet.write(row, 3, data[3], header_format1) #Target Length
#     # worksheet.write(row, 4, data[4], header_format1) #Twists
#     # worksheet.write(row, 5, data[5], header_format1) #Percent Query Aligned
#     # worksheet.write(row, 6, data[6], header_format1) #Percent Target Aligned
#     # # worksheet.write(row, 7, data[7], header_format1) #Init. length
#     # worksheet.write(row, 7, data[8], header_format1) #Opt. Equivalent
#     # # worksheet.write(row, 9, data[9], header_format1) #Init. rmsd
#     # worksheet.write(row, 8, data[10], header_format1) #Opt. rmsd
#     # worksheet.write(row, 9, data[11], header_format1) #Chain rmsd
#     # worksheet.write(row, 10, data[12], header_format1) #p-value
#     # worksheet.write(row, 11, data[13], header_format1) #score
#     # worksheet.write(row, 12, data[14], header_format1) #TotAlign Length
#     # # worksheet.write(row, 15, data[15], header_format1) #Gap Length
#     # worksheet.write(row, 13, data[16], header_format1) #%Gaps of align
#     # # worksheet.write(row, 17, data[17], header_format1) #AFP number
#     # worksheet.write(row, 14, data[18], header_format1) #Identity(%)
#     # worksheet.write(row, 15, data[19], header_format1) #Similarity(%)
#     # worksheet.write(row, 16, data[20], header_format2) # Alignment txt file
#     # worksheet.write(row, 17, data[21], header_format2) #Alignment pdb File
#     # else:
#     #     worksheet.write(row, 0, data[0], right_format) #Query
#     #     worksheet.write(row, 1, data[1], right_format) #Target
#     #     worksheet.write(row, 2, data[2], center_format) #Query Length
#     #     worksheet.write(row, 3, data[3], center_format) #Target Length
#     #     worksheet.write(row, 4, data[4], center_format) #Twists
#     #     worksheet._write(row, 5, float(data[5]), percent_format) #Percent Query Aligned
#     #     worksheet._write(row, 6, float(data[6]), percent_format) #Percent Target Aligned
#     #     # worksheet.write(row, 7, data[7], center_format) #Init. length
#     #     worksheet.write(row, 7, data[8], center_format) #Opt. Equivalent
#     #     # worksheet.write(row, 9, float(data[9]), rmsd_format) #Init. rmsd
#     #     worksheet.write(row, 8, float(data[10]), rmsd_format) #Opt. rmsd
#     #     worksheet.write(row, 9, float(data[11]), rmsd_format) #Chain rmsd
#     #     worksheet.write(row, 10, float(data[12]), sci_format) #p-value
#     #     worksheet.write(row, 11, float(data[13]), percent_format) #score
#     #     worksheet.write(row, 12, data[14], center_format) #TotAlign Length
#     #     # worksheet.write(row, 15, data[15], center_format) #Gap Length
#     #     worksheet.write(row, 13, float(data[16]), percent_format) #%Gaps of align
#     #     # worksheet.write(row, 17, data[17], center_format) #AFP number
#     #     worksheet.write(row, 14, float(data[18]), percent_format) #Identity(%)
#     #     worksheet.write(row, 15, float(data[19]), percent_format) #Similarity(%)
#     #     worksheet.write_url(row, 16, data[20], file_link_format, string=os.path.basename(data[20])) # Alignment txt file
#     #     worksheet.write_url(row, 17, data[21], file_link_format, string=os.path.basename(data[21])) #Alignment pdb File
# # workbook.close()
# # writer.save()




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
