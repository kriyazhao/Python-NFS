import re
import hashlib

class UserValidator:

    def __init__(self, un=None, pw=None):
        self.un = un
        self.pw = pw

    def setUsername(self, un):
        self.un = un
    
    def setPassword(self, pw):
        self.pw = pw

    def usernameValidate(self):
        if self.un != None:
            if re.match("^[A-Za-z0-9_-]{3,16}$", self.un):
                return True
            else:
                return False
        else:
            return False
    
    def passwordValidate(self):
        if self.pw != None:
            if re.match("^[A-Za-z0-9@#$%^&+=]{8,16}$", self.pw):
                return True
            else:
                return False
        else:
            return False
