#==========================================================================================================================
# import python modules
import logging, argparse, ConfigParser
import web, os, platform, ctypes
import hashlib
import shutil
import json

# import customized modules
import fileValidator
import ErrorHandler

#==========================================================================================================================
# Data class for acquiring, creating and deleting file fileContents.
class Data:

    # writePath function writes the file path with hashMd5 and hashSHA1
    def writePath(self, hashMD5, hashSHA1, writeType = "get"): # writeType in "get", "put" and "delete"
        global myConfig, fileCount, session

        # build the hashed path
        increNum = len(hashMD5) // 2
        while not hashMD5[increNum].isdigit():
            increNum += 1
        completePath = "{0}/".format(myConfig.getDataDir())
        dirpath = "{0}/".format(myConfig.getDataDir())
        dirpath += "{0}".format(hashMD5[0:int(hashMD5[increNum])])
        for i in range(0, len(hashMD5), int(hashMD5[increNum])):
            completePath += "{0}/".format(hashMD5[i:i+int(hashMD5[increNum])])
        if writeType == "put":
            return completePath
        elif writeType == "delete":
            return dirpath
        elif writeType == "get":
            completePath += "{0}.obj".format(hashSHA1)
            return completePath
        else:
            raise TypeError("write type cannot be recgnized!")
            return

    # verifyfileContent function verifies if the path can be converted to the hash values
    def verifyfileContent(self, completePath, hashMD5, hashSHA1):
        global myConfig, fileCount, session
   
        # verify the fileContent
        if not os.path.isfile(completePath):
            logging.info("File not found: {0}".format(completePath))
            return ErrorHandler.NotFoundError()
        else:
            with open(completePath, 'rb') as data:
                fileContent = data.read()
            # convert the hashed path and filename to hexadecimal numbers
            myMD5 = hashlib.md5(fileContent).hexdigest()
            mySHA1 = hashlib.sha1(fileContent).hexdigest()
            # to see if hash is verified
            if myMD5 == hashMD5 and mySHA1 == hashSHA1:
                return True
            else:
                return False
            
    # GET function responds to request.get method from the client-side
    def GET(self, hashMD5, hashSHA1):
        global myConfig, fileCount, session
	
	if session.get('logged_in', True):	
            # build the hashed path and read the file
            completePath = self.writePath(hashMD5, hashSHA1, "get")
            # raise error if no such file is found
            verifyResult = self.verifyfileContent(completePath, hashMD5, hashSHA1)
            if verifyResult == True:
                with open(completePath, 'rb') as data:
                    fileContent = data.read()
                    return fileContent
    	    else:
                return ErrorHandler.NotFoundError()
            # return an error if the provided codes doesn't match that of the fileContent
            logging.error("Something is weird about the provided: {0}".format(completePath))
            return ErrorHandler.ServerError()
	else:
            return "please login first!" 
            
    # PUT function responds to request.put method from the client-side
    def PUT(self, hashMD5, hashSHA1):
        global myConfig, fileCount, session

	if session.get('logged_in', True):	
            # get the fileContent data from the client-side
            fileContent = web.data()
            if len(fileContent) > myConfig.getMaxSize():
                # The fileContent is wrong.  Return a 400 bad request error. Log info about the remote in the future.
                logging.warning("fileContent size exceeds the limit!")
                logging.info("actual fileContent size: {0}".format(len(fileContent)))
                logging.info("config fileContent size: {0}".format(myConfig.getMaxSize()))
                return "fileContent size exceeds the limit!"
            # build the hashed path and write the file
            completePath = self.writePath(hashMD5, hashSHA1, "put")
            # create the path if not detected
            if not os.path.exists(completePath):
                os.makedirs(completePath)
            completePath += "{0}.obj".format(hashSHA1)
            # write the file if not detected
            if not os.path.isfile(completePath):
                logging.info("Adding a new fileContent at: {0}".format(completePath))
                with open(completePath, 'wb') as data:
                    data.write(fileContent)
            else:
                logging.info("file already exists: {0}".format(completePath))
                return "file already exists!"
            # read the file again and verify it is hashed correctly
            verifyResult = self.verifyfileContent(completePath, hashMD5, hashSHA1)
            if verifyResult == True:
                fileCount += 1
                return "Successfully add the fileContent!"
            else:
                return ErrorHandler.NotFoundError()
            # return an error if the provided codes doesn't match that of the fileContent
            logging.error("Something is weird about the provided: {0}".format(completePath))
            return ErrorHandler.ServerError()
        else:
            return "please login first!"

    # DELETE function responds to request.delete method from the client-side
    def DELETE(self, hashMD5, hashSHA1):
        global myConfig, fileCount, session
        
	if session.get('logged_in', True):	
            # build the hashed path 
            completePath = self.writePath(hashMD5, hashSHA1)
            # raise error if no such file is found
            vertifyResult = self.verifyfileContent(completePath, hashMD5, hashSHA1)
            if vertifyResult == True:
                dirpath = self.writePath(hashMD5, hashSHA1, "delete")
                shutil.rmtree(dirpath)
                fileCount -= 1
                return "Successfully delete the fileContent!"
            else:
                return ErrorHandler.NotFoundError()
            # return an error if the provided codes doesn't match that of the fileContent
            logging.error("Something is weird about the provided: {0}".format(completePath))
            return ErrorHandler.ServerError()
        else:
            return "please login first!"

    # POST function responds to request.post method from the client-side
    def POST(self, hashMD5, hashSHA1):
        global myConfig, fileCount, session
        
	if session.get('logged_in', True):	
            # build the hashed path
            completePath = self.writePath(hashMD5, hashSHA1)
            # verify fileContent 
            vertifyResult = self.verifyfileContent(completePath, hashMD5, hashSHA1)
            if vertifyResult == True:
                requestCon = web.data()
                requestContent = json.loads(requestCon)
                logging.info("requestContent: {0}".format(requestContent))
                logging.info("type: {0}".format(type(requestContent)))
                if "insert" in requestContent:
                    with open(completePath, 'r+') as data:
                        oldfileContent = data.read()
                        logging.info("insert oldfileContent: {0}".format(oldfileContent))
                    for i in requestContent["insert"]:
                        newfileContent = oldfileContent[0:int(i[0])] + i[1] + oldfileContent[int(i[0])+1:]
                        logging.info("insert newfileContent: {0}".format(newfileContent))
                        with open(completePath, 'w+') as data:
                            data.write(newfileContent)
                if "modify" in requestContent:
                    with open(completePath, 'r+') as data:
                        oldfileContent = data.read()				
                    for i in requestContent["modify"]:
                        newfileContent = oldfileContent[0:int(i[0])] + i[2] + oldfileContent[int(i[1])+1:]
                        with open(completePath, 'w+') as data:
                            data.write(newfileContent)
                if "delete" in requestContent:
                    with open(completePath, 'r+') as data:
                        oldfileContent = data.read()
                    for i in requestContent["delete"]:
                        newfileContent = oldfileContent[0:int(i[0])] + oldfileContent[int(i[1])+1:]
                        with open(completePath, 'w+') as data:
                            data.write(newfileContent)
                logging.info("Successfully update the file!")
                # rewrite hash path and filename for the updated file 
                with open(completePath, 'rb') as data:
                    fileContent = data.read()
                myMD5 = hashlib.md5(fileContent).hexdigest()
                mySHA1 = hashlib.sha1(fileContent).hexdigest()
                newPath = self.writePath(myMD5, mySHA1, "put")
                if not os.path.exists(newPath):
                    os.makedirs(newPath)
                newPath += "{0}.obj".format(hashSHA1)
                if not os.path.isfile(newPath):
                    logging.info("Adding a new fileContent at: {0}".format(newPath))
                    with open(newPath, 'wb') as result:
                        result.write(fileContent)
                else:
                    return "new file already exists!"
                # delete the original path and file
                dirpath = self.writePath(hashMD5, hashSHA1, "delete")
                shutil.rmtree(dirpath)
                logging.info("Deleting the old fileContent at: {0}".format(completePath))
                return fileContent
            else:
                return ErrorHandler.NotFoundError()
            # return an error if the provided codes doesn't match that of the fileContent
            logging.error("Something is weird about the provided: {0}".format(completePath))
            return ErrorHandler.ServerError()
        else:
            return "please login first!"
