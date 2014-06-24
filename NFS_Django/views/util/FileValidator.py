#==========================================================================================================================
# import python modules
import os
import re
from NFS_Django.views.util.EncryptionPath import EncryptionPath
from NFS_Django.views.util.FileNotepad import FileNotepad 

class FileValidator:
    
    def __init__(self, completePath=None, filename=None):
        self.completePath = completePath
        self.filename = filename
        
    def setfilePath(self, completePath):
        self.completePath = completePath
    
    def setfileName(self, filename):
        self.filename = filename

    def verifyfileName(self):
        if self.filename != None:
            if re.match("[^/]{1,50}\.(txt|log|ini|h|hpp|c|cpp|java|html|htm|php|js|jsp|asp|css|xml|sh;*.bsh|pl|pm|rb|py|rc|sql|nfo|mak|reg)$", self.filename):
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
        if len(filecontent) > 5*1024*1024:
            logging.warning("fileContent size exceeds the limit!")
            return False
        else:
            return True

    # verifyfileContent function verifies if the path can be converted to the hash values
    def verifyfileContent(self, hashSHA1):
        if self.completePath != None:
            readfile = FileNotepad()
            readfile.setFilepath(self.completePath)
            encryptSHA1 = EncryptionPath()
            fileContent = readfile.readFile()
            # convert the hashed path and filename to hexadecimal numbers
            mySHA1 = encryptSHA1.creatSHA1(fileContent)
            if mySHA1 == hashSHA1:
                return True
            else:
                return False