def renderPDB(inputPDB):
    import pymol
    import os.path
    import re

    print("[renderPDB]: ", inputPDB)
    objName = os.path.basename(inputPDB).rstrip(".pdb")
    ## strip some characters pymol cant use:
    objName = re.sub("[)]", "_", objName)
    objName = re.sub("[(]", "_", objName)
    pymol.cmd.load(inputPDB)
    print("[renderPDB]: load")
    pymol.cmd.split_chains(objName)
    pymol.cmd.color("blue", str(objName + "_T"))
    pymol.cmd.color("orange", str(objName + "_Q"))
    pymol.cmd.hide("all")
    pymol.cmd.show("ribbon")
    pymol.cmd.delete(objName)
    pymol.cmd.set('ray_opaque_background', 1)
    pymol.cmd.set('ray_trace_fog', 0)
    pymol.cmd.set ('ray_shadows', 0)
    pymol.cmd.set ('antialias', 1)
    pymol.cmd.set('orthoscopic', 0)
    pymol.cmd.bg_color("white")
    pymol.cmd.png(inputPDB.rstrip(".pdb") + ".png", height="6in", width="6in", ray=1, dpi=400)
    # pymol.cmd.png(objName + ".png", height="6in", width="6in", ray=1, dpi=400)
    pymol.cmd.save(inputPDB.rstrip(".pdb") + ".pse", format="pse")
    # pymol.cmd.save(objName + ".pse", format="pse")
    # print(name)

def renderPdbBatch(outputDirRoot, cores):
    import multiprocessing as mp
    import os
    import glob

    ### adjust number of cores
    if cores >= int(mp.cpu_count()):
        optCores = int(mp.cpu_count())-1
        print("Too many cores selected")
        print("Reducing to " + str(optCores) + " cores")
        cores = optCores
    if cores < int(mp.cpu_count()):
        cores = cores

    ## detect 'fcWriteTemp' and create batches
    FilesToProcess = []
    for root, dirs, files in os.walk(outputDirRoot):
        # print(root, dirs)
        for file in files:
            # print(root, dirs)
            if "_alignment.pdb" in file: ## look for fcWriteTemp folder
                # DirsToProcess.append(root + "/" + dir)
                # print(root, dirs, file)
                FilesToProcess.append(root + "/" + file)
    # print(FilesToProcess)

    # for d in DirsToProcess:
    #     print(d)

    batchDict = {}
    b = 1
    for i in range(0, len(FilesToProcess), cores):
        batchName = "b"+str(b)
        batchDict[batchName] = FilesToProcess[i:i + cores]
        b = b + 1
    # print(batchDict)


    ### multiprocess with resultSummarization.pandasToXls
    for key, values in batchDict.items():
        print("[renderPdbBatch]: Processing batch ", key, " of ", len(batchDict))
        procs = []
        # if key == "b1":
        #     print(key, values)
        #     for d in values:
        #         print(d)
        if key:
            for inputPDB in values:
                # print(inputPDB)
                # single argument requires a "," after
                # see: https://stackoverflow.com/questions/1559125/string-arguments-in-python-multiprocessing
                p = mp.Process(target=renderPDB, args=(inputPDB,))
                procs.append(p)
                # print(p)
                p.start()
            for proc in procs:
                proc.join()
