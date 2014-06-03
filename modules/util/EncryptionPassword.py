import hashlib

class EncryptionPassword:
    
    def __init__(self, pw=None):
        self.pw = pw

    def setPassword(self, pw):
        self.pw = pw

    def encryptPw(self):
        if self.pw != None:
            hashPw = hashlib.md5(self.pw).hexdigest()
            return hashPw
        else:
            return None