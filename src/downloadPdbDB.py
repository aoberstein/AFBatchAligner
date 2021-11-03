def downloadPdbDB(dbWriteFolder, rsyncFullPath):
    import os
    import subprocess

    if os.path.exists(dbWriteFolder):
        pass
    else:
        os.mkdir(dbWriteFolder, mode=0o755)

    proc = subprocess.Popen([rsyncFullPath, '-rlpt', '-v', '-z', '--delete',
        '--port=33444', 'rsync.wwpdb.org::ftp_data/structures/divided/pdb/',
        dbWriteFolder], bufsize=-1)

