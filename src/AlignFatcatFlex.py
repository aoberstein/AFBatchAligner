def jFatCatAlign(queryPDB, targetPDB, javaFullPath, aoFatCatJar,
                 outputDir, alignmentCutoff = 0.05):
    import os
    import subprocess
    if os.path.exists(outputDir):
        pass
    else:
        os.mkdir(outputDir, mode = 0o755)
    proc = subprocess.Popen([javaFullPath, '-jar', aoFatCatJar,
                             queryPDB, targetPDB, str(alignmentCutoff), outputDir],
                            bufsize=-1)
    code=proc.wait()
    # if str(code) == '0':
        # print("[jFatCatAlign]: Success")
    # else:
        # print("[jFatCatAlign]: Failed")


def fatcatMultiProcess(queryPDB, targetPDBList, javaFullPath, aoFatCatJar,
                       outputDir, alignmentCutoff = 0.05, cores = 4):
    import multiprocessing as mp
    import os
    import sys
    import time

    if cores >= int(mp.cpu_count()):
        optCores = int(mp.cpu_count())-1
        # print("Too many cores selected")
        # print("Reducing to " + str(optCores) + " cores")
        cores = optCores
    if cores < int(mp.cpu_count()):
        cores = cores

    ### create output subdirectories
    # check for outputDir and create if absent
    if os.path.exists(outputDir):
        pass
    else:
        os.mkdir(outputDir, mode = 0o755)

    # query = os.basename(queryPDB)
    queryPrefix = os.path.basename(queryPDB).rstrip(".pdb")
    subDir = outputDir+"/"+queryPrefix
    if os.path.exists(subDir):
        pass
    else:
        os.mkdir(subDir, mode = 0o755)

    file = open(targetPDBList, 'r')
    lines = file.readlines()
    ts = time.time()

    with open(os.devnull, 'w') as devnull:
        # suppress stdout
        orig_stdout_fno = os.dup(sys.stdout.fileno())
        os.dup2(devnull.fileno(), 1)
        # suppress stderr
        orig_stderr_fno = os.dup(sys.stderr.fileno())
        os.dup2(devnull.fileno(), 2)
        pool = mp.Pool(processes=cores)
        # for targetPDB in lines[:309]:
        for targetPDB in lines:
            targetPDB = targetPDB.strip()
            pool.apply_async(func=jFatCatAlign,
                             args=(queryPDB, targetPDB, javaFullPath, aoFatCatJar, subDir, alignmentCutoff))
        pool.close()
        pool.join()
    os.dup2(orig_stdout_fno, 1)  # restore stdout
    os.dup2(orig_stderr_fno, 2)  # restore stderr
    print('Time in parallel:', time.time() - ts)

