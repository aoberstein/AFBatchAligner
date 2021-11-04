def checkFolderBackslash(Dir):
    '''
    helper function for pdbTools.exportPdbToLengths
    '''
    import re
    if re.match(".*[/]$", Dir):
        # print("FOUND:" + Dir)
        return Dir
    else:
        # print("ADDING BACKSLASH:" + Dir)
        return Dir + "/"