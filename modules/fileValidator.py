#==========================================================================================================================
# import python modules
import logging, argparse, ConfigParser
import web, os, platform, ctypes
import hashlib
import shutil
import json
import datetime

#==========================================================================================================================
# A function to check the status of current files in the dataDir to see if they've been changed and return the number of files
def fileValidator(path):
    global myConfig, fileCount, session, db

    fileCount = 0
    results = db.query("SELECT md5code,sha1code FROM file")
    rows = list(results)
    for row in rows:
        validateFile = True
        myMD5 = row['md5code']
        mySHA1 = row['sha1code']
        # write the path with a strategy
        increNum = len(myMD5) // 2
        while not myMD5[increNum].isdigit():
            increNum += 1
        currentPath = "{0}/".format(myConfig.getDataDir())
        for i in range(0, len(myMD5), int(myMD5[increNum])):
            currentPath += "{0}/".format(myMD5[i:i+int(myMD5[increNum])])
            # check the filepath
        if not os.path.exists(os.path.abspath(currentPath)):
            # The hashed path cannot be matched to that of the original file.
            logging.warning("The file path has been modified!!!")
            logging.info("	currentPath: {0}".format(os.path.abspath(currentPath)))
            validateFile = False
        # check the filename
        currentFile = currentPath + "{0}.obj".format(mySHA1)
        if not os.path.exists(os.path.abspath(currentFile)):
            # The hashed filename cannot be matched to that of the original file.
            logging.warning("The file name has been modified!!!")
            logging.info("	currentFile: {0}".format(currentFile))
            validateFile = False
        # increment the fileCount if no modification is detected for the files
        if validateFile == True:
            fileCount += 1
        # delete the files that have been modified by others
        else:
            db.update("file", where="md5code=$myMD5 AND sha1code=$mySHA1", abnormality=1,
                      vars={'myMD5':myMD5, 'mySHA1':mySHA1})
    return fileCount
