#==========================================================================================================================
# import python modules
import logging, argparse, ConfigParser
import web, os, platform, ctypes
import hashlib
import shutil
import json
import datetime

#==========================================================================================================================
# EncryptionPath class for writing encrypted path and varify files
class EncryptionPath:
    global myConfig, fileCount, session, db

    # writePath function writes the file path with hashMd5 and hashSHA1
    def writePath(self, hashMD5, hashSHA1, writeType = "get"): # writeType in "get", "put" and "delete"
        # build the hashed path
        if not (hashMD5 == 0 or hashSHA1 == 0):
            increNum = len(hashMD5) // 2
            while not hashMD5[increNum].isdigit():
                increNum += 1
            completePath = "{0}/".format(myConfig.getDataDir())
            dirpath = "{0}/".format(myConfig.getDataDir())
            dirpath += "{0}".format(hashMD5[0:int(hashMD5[increNum])])
            for i in range(0, len(hashMD5), int(hashMD5[increNum])):
                completePath += "{0}/".format(hashMD5[i:i+int(hashMD5[increNum])])
            if writeType == "put": # only return the directory of the file
                return completePath
            elif writeType == "delete": # only return the first-level directory of the file
                return dirpath
            elif writeType == "get": # return the directory + filename of the file
                completePath += "{0}.obj".format(hashSHA1)
                return completePath
            else:
                raise TypeError("write type cannot be recgnized!")
                return
        else:
            raise ValueError("hash code is empty!")

    # verifyfileContent function verifies if the path can be converted to the hash values
    def verifyfileContent(self, completePath, hashMD5, hashSHA1):
        # verify the fileContent
        if not os.path.isfile(completePath):
            logging.info("File not found: {0}".format(completePath))
            return self.NotFoundError()
        else:
            with open(completePath, 'rb') as data:
                fileContent = data.read()
            # convert the hashed path and filename to hexadecimal numbers
            mySHA1 = hashlib.sha1(fileContent).hexdigest()
            # to see if hash is verified
            if mySHA1 == hashSHA1:
                return True
            else:
                return False
