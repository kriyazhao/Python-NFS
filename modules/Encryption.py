

#
class Encryption:

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
