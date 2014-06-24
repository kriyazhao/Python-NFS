import re
import hashlib

class MD5Validator:

    def __init__(self, md5=None):
        self.md5 = md5

    def setHashCode(self, md5):
        self.md5 = md5

    def MD5Validate(self):
        if self.md5 != None:
            if re.findall(r"([a-f\d]{32})", self.md5):
                return True
            else:
                return False
        else:
            return False
