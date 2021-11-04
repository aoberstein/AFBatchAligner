###

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
    # print(subDir)
    files = glob.glob(subDir + "*_fcLine.tab")
    # print(files)
    header = ["Query", "Target", "Query Length", "Target Length",
             "Twists", "Percent Query Aligned", "Percent Target Aligned",
             "Init. length", "Opt. Equiv.", "Init. rmsd", "Opt. rmsd",
             "Chain rmsd", "p-value", "score", "TotAlign Length", "Gap Length",
             "%Gaps of align", "AFP number", "Ident. (%)", "Similar (%)",
             "Alignment txt File", "Alignment PSE File"]

    ## coerce lists of lists to pd.DataFrame (allows sorting)
    outLines = []
    outLines.append(header)
    for file in files:
        handle = open(file, "r")
        stats = handle.readlines()[1]
        # print(stats)
        stats = stats.strip()
        stats = re.sub("\s+", "\t", stats)
        statList = stats.split('\t')
        pdb1 = stats.split('\t')[0]
        pdb2 = stats.split('\t')[1]
        pdbFile = Dir + "/" + pdb1 + "_" + pdb2 + "_alignment.pdb"
        txtFile = Dir + "/" + pdb1 + "_" + pdb2 + "_FatCat.txt"
        statList.append(txtFile)
        statList.append(pdbFile)
        outLines.append(statList)
    # print(outLines)
    df = pandas.DataFrame(columns = outLines[0], data = outLines[1:])

    ## sort df
    df["score"] = pandas.to_numeric(df["score"])
    df.sort_values(by="score", ascending=False, inplace=True)
    # print(df['score'])

    ## remove some columns
    df = df.drop(columns=['Init. length', 'Init. rmsd', 'Gap Length', 'AFP number'])

    # ## convert NaN to "0":
    # df = df.fillna(0)

    ## coerce back to list of lists
    # allows greater control over formatting (e.g. multi-formatting of header cells)
    # using pandas allows sorting prior to generating the excel file
    header = df.columns.tolist()
    outLines = df.values.tolist()
    
    ## write formatted xls file
    writeDir = Dir
    workbook = xlsxwriter.Workbook(writeDir + "0_" + queryPrefix + "_summary.xlsx", {'nan_inf_to_errors': True})
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
    file_link_format = workbook.add_format({'bold': False, 'underline': True, 'font_color': 'blue'})
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
    worksheet.write(0, 17, header[17], header_format2) #Alignment pse File

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
        worksheet.write_url(row, 17, data[17].rstrip(".pdb")+".pse", file_link_format,
                            string=os.path.basename(data[17]).rstrip(".pdb")+".pse") #Alignment pse File

    workbook.close()
    

def pandasToXlsBatch(outputDirRoot, cores):
    import multiprocessing as mp
    import os

    ### adjust number of cores
    if cores >= int(mp.cpu_count()):
        optCores = int(mp.cpu_count())-1
        # print("Too many cores selected")
        # print("Reducing to " + str(optCores) + " cores")
        cores = optCores
    if cores < int(mp.cpu_count()):
        cores = cores

    ## detect 'fcWriteTemp' and create batches
    DirsToProcess = []
    for root, dirs, files in os.walk(outputDirRoot):
        # print(root, dirs)
        for dir in dirs:
            # print(root, dirs)
            if 'fcWriteTemp' in dir:
                # DirsToProcess.append(root + "/" + dir)
                DirsToProcess.append(root)

    # for d in DirsToProcess:
    #     print(d)

    batchDict = {}
    b = 1
    for i in range(0, len(DirsToProcess), cores):
        batchName = "b"+str(b)
        batchDict[batchName] = DirsToProcess[i:i + cores]
        b = b + 1
    # print(batchDict)

    ### multiprocess with resultSummarization.pandasToXls
    for key, values in batchDict.items():
        procs = []
        # if key == "b1":
        #     print(key, values)
        #     for d in values:
        #         print(d)
        if key:
            for Dir in values:
                # print(type(Dir))
                # single argument requires a "," after
                # see: https://stackoverflow.com/questions/1559125/string-arguments-in-python-multiprocessing
                p = mp.Process(target=pandasToXls, args=(Dir,))
                procs.append(p)
                # print(p)
                p.start()
            for proc in procs:
                proc.join()

