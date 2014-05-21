#==========================================================================================================================
# import python modules
import logging, argparse, ConfigParser
import web, os, platform, ctypes
import hashlib
import shutil
import json

# import customized modules
import ErrorHandler
import Encryption

#==========================================================================================================================
# A function to check the status of current files in the dataDir to see if they've been changed and return the number of files
def fileValidator(self, path):
    global myConfig, fileCount, session

    fileCount = 0
    for root, dir, files in os.walk(path):
        logging.info("validateFiles: root:  {0}".format(root))
        logging.info("validateFiles: dir:   {0}".format(str(dir)))
        logging.info("validateFiles: files: {0}".format(str(files)))
        for currentFile in files:
            validateFile = True
            logging.info("validateFiles: currentFile: {0}".format(currentFile))
            # read the content of the file
            fileContent = open(os.path.abspath("{0}/{1}".format(root, currentFile)), 'rb').read()
            # hash the fileContent
            myMD5 = hashlib.md5(fileContent).hexdigest()
            mySHA1 = hashlib.sha1(fileContent).hexdigest()
            # write the path with a strategy
            currentPath = Encryption.writePath(myMD5, mySHA1, "get")
            dirpath = Encryption.writePath(myMD5, mySHA1, "delete")
            # check the filepath
            if os.path.abspath(currentPath) != os.path.abspath(root):
                # The hashed path cannot be matched to that of the original file.
                logging.warning("The file path has been modified!!!")
                logging.info("	root:    {0}".format(os.path.abspath(root)))
                logging.info("	currentPath: {0}".format(os.path.abspath(currentPath)))
                validateFile = False
            # check the filename
            if currentFile != "{0}.obj".format(mySHA1):
                # The hashed filename cannot be matched to that of the original file.
                logging.warning("The file name has been modified!!!")
                logging.info("	currentFile: {0}".format(currentFile))
                logging.info("	mySHA1:  {0}".format(mySHA1))
                validateFile = False
            # increment the fileCount if no modification is detected for the files
            if validateFile == True:
                fileCount += 1
            # delete the files that have been modified by others
            else:
                logging.warning("Deleting the files that has been modified by others!")
                shutil.rmtree(dirpath)
    return fileCount
