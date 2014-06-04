#==========================================================================================================================
# import python modules
import hashlib

import 

#==========================================================================================================================
# EncryptionPath class for writing encrypted path
class EncryptionPath:
    global myConfig, fileCount
    
    def __init__(self):
        self.hashMD5 = 0
        self.hashSHA1 = 0
    
    def setHashCode(self, md5, sha1):
        self.hashMD5 = md5
        self.hashSHA1 = sha1
    
    # creatMD5 function writes md5 code
    def creatMD5(self, filename, filecontent, userid):
        self.hashMD5 = str(hashlib.md5(filename + filecontent).hexdigest()) + str(userid)
        return self.hashMD5
        
    # creatSHA1 function writes sha1 code
    def creatSHA1(self, filecontent):
        self.hashSHA1 = str(hashlib.sha1(filecontent).hexdigest())
        return self.hashSHA1

    # writePath function writes the file path with hashMd5 and hashSHA1
    def writePath(self, writeType = "get"): # writeType in "get", "put" and "delete"
        # build the hashed path
        if not (self.hashMD5 == 0 or self.hashSHA1 == 0):
            increNum = len(self.hashMD5) // 2
            while not self.hashMD5[increNum].isdigit():
                increNum += 1
            completePath = "{0}/".format(myConfig.getDataDir())
            dirpath = "{0}/(1)".format(myConfig.getDataDir(), self.hashMD5[0:int(self.hashMD5[increNum])])
            for i in range(0, len(self.hashMD5), int(self.hashMD5[increNum])):
                completePath += "{0}/".format(self.hashMD5[i:i+int(self.hashMD5[increNum])])
            if writeType == "put": # only return the directory of the file
                return completePath
            elif writeType == "delete": # only return the first-level directory of the file
                return dirpath
            elif writeType == "get": # return the directory + filename of the file
                completePath += "{0}.obj".format(self.hashSHA1)
                return completePath
            else:
                raise TypeError("write type cannot be recgnized!")
                return
        else:
            raise ValueError("hash code is empty!")