import hashlib
import os
from NFS_Django.views.model.UserModel import UserModel
import logging
logging.basicConfig(level=logging.INFO)
class EncryptionPassword:
    
    def __init__(self, pw=None):
        self.pw = pw

    def setPassword(self, pw):
        self.pw = pw

    def encryptPw(self, salt=None):
        if self.pw != None:
            if salt == None:
                rawSalt = os.urandom(32)
                hexSalt = hashlib.md5(rawSalt).hexdigest()
            else:
                hexSalt = salt
            hashPw = hashlib.md5(self.pw+hexSalt).hexdigest()
            return [hashPw,hexSalt]
        else:
            return None