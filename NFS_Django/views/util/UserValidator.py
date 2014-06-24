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
            if re.match("^[a-zA-Z][a-zA-Z0-9._-]{3,20}$", self.un):
                return True
            else:
                return False
        else:
            return False
    
    def passwordValidate(self):
        if self.pw != None:
            if re.match("^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*])[0-9a-zA-Z!@#$%^&*]{8,}$", self.pw):
                return True
            else:
                return False
        else:
            return False
