import unittest
import json
import sys
sys.path.append("/var/www/fs/NFS_Django/")
from NFS_Django.views.util.UserValidator import UserValidator

class TestPasswordValidator(unittest.TestCase):

    def setUp(self): 
        print self._testMethodName + " begins now......"
        self.validator = UserValidator()
    
    def test_password_empty_fail(self):
        self.validator.setPassword("")
        self.assertFalse(self.validator.passwordValidate())
        
    def test_password_onlynum_fail(self):
        self.validator.setPassword("12345")
        self.assertFalse(self.validator.passwordValidate())

    def test_password_onlyletter_fail(self):
        self.validator.setPassword("tiAADfes")
        self.assertFalse(self.validator.passwordValidate())

    def test_password_short_fail(self):
        self.validator.setPassword("tA12")
        self.assertFalse(self.validator.passwordValidate())
        
    def test_password_valid_success(self):
        self.validator.setPassword("ting123!A")
        self.assertTrue(self.validator.passwordValidate())
  
    def tearDown(self):
        del self.validator
    
if __name__ == "__main__":
    unittest.main()