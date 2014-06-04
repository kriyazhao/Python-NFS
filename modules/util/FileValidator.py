#==========================================================================================================================
# import python modules
import os
import re

import FileNotepad, EncryptionPath

class FileValidator:
    global myConfig
    
    def __init__(self, completePath=None):
        self.completePath = completePath
        self.filename = os.path.basename(self.completePath)
        
    def setfilePath(self, completePath):
        self.completePath = completePath
    
    def setfileName(self, filename):
        self.filename = filename

    def verifyfileName(self):
        if self.filename != None:
            if re.match("^[A-Za-z0-9_-].txt$", self.filename):
                return True
            else:
                return False

    def verifyfilePath(self):
        if self.completePath != None:
            if os.path.isfile(self.completePath):
                return True
            else:
                return False    
    
    def verifyfileSize(self, filecontent):
        if len(fileContent) > myConfig.getMaxSize():
            logging.warning("fileContent size exceeds the limit!")
            return False
        else:
            return True

    # verifyfileContent function verifies if the path can be converted to the hash values
    def verifyfileContent(self, hashSHA1):
        if self.completePath != None:
            self.readFile = FileNotepad(self.completePath)
            self.encryptSHA1 = EncryptionPath()
            fileContent = self.readFile.readFile()
            # convert the hashed path and filename to hexadecimal numbers
            mySHA1 = self.encryptSHA1.creatSHA1(fileContent)
            if mySHA1 == hashSHA1:
                return True
            else:
                return False