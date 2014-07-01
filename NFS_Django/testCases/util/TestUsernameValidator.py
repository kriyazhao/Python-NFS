import unittest
import json
import sys
sys.path.append("/var/www/fs/NFS_Django/")
from NFS_Django.views.util.UserValidator import UserValidator

class TestUsernameValidator(unittest.TestCase):

    def setUp(self): 
        print self._testMethodName + " begins now......"
        self.validator = UserValidator()
    
    def test_username_empty_fail(self):
        self.validator.setUsername("")
        self.assertFalse(self.validator.usernameValidate())
        
    def test_username_onlynum_fail(self):
        self.validator.setUsername("12345")
        self.assertFalse(self.validator.usernameValidate())

    def test_username_startsnum_fail(self):
        self.validator.setUsername("12345ting")
        self.assertFalse(self.validator.usernameValidate())

    def test_username_short_fail(self):
        self.validator.setUsername("ti")
        self.assertFalse(self.validator.usernameValidate())
        
    def test_username_valid_success(self):
        self.validator.setUsername("ting123")
        self.assertTrue(self.validator.usernameValidate())
  
    def tearDown(self):
        del self.validator
    
if __name__ == "__main__":
    unittest.main()
